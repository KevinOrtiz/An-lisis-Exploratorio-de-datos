# -*- encoding: utf-8 -*-

__author__ = 'josanvel'

import re
import time
from scrapy.spider import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy import selector, loader
from scrapy_hotel.items import *
from crawlerhelper import *
import scrapy

# Constants.
# Max reviews pages to crawl.
# Reviews collected are around: 5 * MAX_REVIEWS_PAGES
MAX_REVIEWS_PAGES = 1000

class tripAdvisorScrapper(BaseSpider):
	name = "tripadvisor_hotel"
	allowed_domains = ["tripadvisor.com"]
	base_uri = "http://www.tripadvisor.com"
	start_urls = [
		base_uri + "/Attractions-g294308-Activities-Quito_Pichincha_Province.html"
	]


	# Entry point for BaseSpider.
	# Page type: /BuscaCosasQueHacer
	def parse(self, response):
		sel = Selector(response)
		#Selector de todos las Actividades
		snode_cosas_que_hacers = sel.xpath('.//div[@id="ATTRACTION_FILTER"]//div[starts-with(@class, "filter filter_xor")]')
		counter_page_actividades = 0

		# Iteracion de cada actividad en la pagina semilla
		for snode_cosas_que_hacer in snode_cosas_que_hacers:
			#========Obtener la URL de la categoria de las Actividades
			name_categoria = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './a//span[contains(@class, "filter_name")]/text()'))
			url_name_categoria = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './a/@href'))
			print name_categoria,'--',url_name_categoria
				
			if url_name_categoria:
				#========Concatenar la URL del Actividades
				url_name_categoria = self.base_uri + url_name_categoria
				yield Request(url=url_name_categoria, meta={'counter_page_actividades' : counter_page_actividades}, callback=self.parse_page_tags)
			

	def parse_page_tags(self, response):
		sel = Selector(response)
		#Selector de todos las Actividades
		counter_page_actividades = response.meta['counter_page_actividades']
		snode_cosas_que_hacers = sel.xpath('//div[@id="FILTERED_LIST"]//div[starts-with(@class, "entry")]')

		#  Limite maximo de reviews de las paginas para crawling
		if counter_page_actividades < MAX_REVIEWS_PAGES:
			#Contador de paginacion principal
			counter_page_actividades = counter_page_actividades + 1

			# Iteracion de cada actividad en la pagina semilla
			for snode_cosas_que_hacer in snode_cosas_que_hacers:
				#========Instanciar el item Actividades
				tripadvisor_item = TripAdvisorItemCosasHacer()
				#========Obtener la URL de la Actividades
				url_name_actividad = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './div[contains(@class, "property_title")]/a/@href'))
				#========Obtener el nombre del Actividades
				tripadvisor_item['name_actividad'] = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './div[contains(@class, "property_title")]/a/text()'))
				#========Obtener el numero de opiniones de la Actividad
				tripadvisor_item['opinions_actividad'] = clean_parsed_string(get_parsed_int(snode_cosas_que_hacer, './div[@class="wrap"]/div[@class="rs rating"]/span[contains(@class,"more")]/a/text()'))
				#========Obtener el rating de la Actividad
				tripadvisor_item['rating_actividad'] = clean_parsed_string(get_parsed_int(snode_cosas_que_hacer, './div[@class="wrap"]/div[@class="rs rating"]/span[contains(@class,"rate")]/img/@alt'))
				
				if url_name_actividad:
				  #========Concatenar la URL del Actividades
				  url_name_actividad = self.base_uri + url_name_actividad
				  yield Request(url=url_name_actividad, meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page)
				
			#Obtener la URL de la pagina siguiente (PAGINACION)
			next_page_actividades = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next rndBtn ui_button primary taLnk")]/@href'))

			if next_page_actividades and len(next_page_actividades) > 0:
			  #========Concatenar la URL de la paginacion de Actividades
			  url_actividades = self.base_uri + next_page_actividades
			  yield Request(url=url_actividades, meta={'counter_page_actividades' : counter_page_actividades}, callback=self.parse_page_tags)


	# Buscar los raiting, ubucacion y los links de los reviews.
	# Page type: /Activiades_Review
	def parse_search_page(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)
		#========Lista el review del Actividades
		tripadvisor_item['reviews_actividad'] = []
		#========Obtener las coordenadas geograficas de la Actividad
		lng = clean_parsed_string(get_parsed_string(sel, '//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lng'))
		lat = clean_parsed_string(get_parsed_string(sel, '//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lat'))

		coordinates = [str(lng), str(lat)]      #Almacena la Longitud y la Latitud del Actividades y lo guarda en una lista

		if lng and lat:  
			#========Obtener la ubicacion del Actividades
			tripadvisor_item['location_actividad'] = coordinates

			#========Obtener el tag del Actividades
			list_tags = []
			#========Obtengo el selector de tags//
			tags = sel.xpath('//*[@id="HEADING_GROUP"]/div/div[3]/div/div[@class="detail"]/a')
			for tag in tags:
				#===============Obtengo string del tag
				elem = clean_parsed_string(get_parsed_string(tag, './text()'))
				#===============Almaceno el tag en una lista de tags
				list_tags.append(elem)

			#========Obtener los tags de Actividades
			tripadvisor_item['tags_categorias_actividades'] = list_tags
			
			url_name_review = clean_parsed_string(get_parsed_string(sel, '//*[@id="REVIEWS"]/div[contains(@class, "reviewSelector")]//div[@class="quote"]/a/@href'))
			if url_name_review:
				#========Concatenar la URL del titulo del review
				url_review = self.base_uri + url_name_review
				yield Request(url=url_review,  meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review' : 0}, callback=self.parse_fetch_review)
			#Aunque no tenga Review aun asi se guarda registro de la Actividad
			else: 
				yield tripadvisor_item
		

	# Si la pagina encuentra un review, hace su analisis exahustivo.
	# Page type: /ShowUserReviews
	def parse_fetch_review(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		counter_page_review = response.meta['counter_page_review']
		sel = Selector(response)

		# Limite maximo de reviews de las paginas para crawling.
		if counter_page_review < MAX_REVIEWS_PAGES:
			counter_page_review = counter_page_review + 1

			# TripAdvisor reviews for item.
			snode_reviews = sel.xpath('//div[@id="REVIEWS"]/div[contains(@class, "reviewSelector")]')

			# Reviews for item.
			contador_mensajes = 0
			for snode_review in snode_reviews:
				if snode_review:
					#========Instanciar el item del review de la Actividad
					tripadvisor_review_item = TripAdvisorReviewItem()
					#========Obtener el titulo del review de la Actividad
					tripadvisor_review_item['title_review'] 		= clean_parsed_string(get_parsed_string(snode_review, './/div[@class="quote"]/a/span/text()'))
					if tripadvisor_review_item['title_review'] is None:
						tripadvisor_review_item['title_review'] 	= clean_parsed_string(get_parsed_string(snode_review, './/div[@class="quote"]/text()'))
				
					#========Obtener la descripcion de un review de la Actividad
					tripadvisor_review_item['description_review'] 	= get_parsed_string_multiple(snode_review, './/div[@class="entry"]/p/text()')

					if tripadvisor_review_item['title_review'] and  tripadvisor_review_item['description_review']:
						contador_mensajes = contador_mensajes + 1
						
						#========Obtener el rating de un review de la Actividad
						tripadvisor_review_item['rating_review'] 		= clean_parsed_string(get_parsed_int(snode_review, './/div[contains(@class,"rating reviewItemInline")]/span/img/@alt'))
						
						#========Obtener el dia de publicacion de un review de la Actividad
						tripadvisor_review_item['date_review'] 			= clean_parsed_string(get_parsed_date(snode_review, './/span[contains(@class,"ratingDate")]/@title'))
						if not tripadvisor_review_item['date_review']:
							tripadvisor_review_item['date_review'] 		= clean_parsed_string(get_parsed_date(snode_review, './/span[contains(@class,"ratingDate")]/text()'))

						#========Obtener la descripcion de un review de la Actividad
						tripadvisor_review_item['username_review'] 		= clean_parsed_string(get_parsed_string(snode_review, './/div[@class="username mo"]/span/text()'))
						#========Obtener la ubicacion del usuario  del review -- Actividad
						tripadvisor_review_item['location_review'] 		= clean_parsed_string(get_parsed_string(snode_review, './/div[contains(@class,"member_info")]//div[@class="location"]/text()'))
						#========Obtener el numero de opinios del usuario  del review -- Actividad
						
						tripadvisor_review_item['opinions_user_review'] = clean_parsed_string(get_parsed_int(snode_review, './/div[contains(@class,"memberBadging")]//div[contains(@class,"contributionReviewBadge")]/span/text()'))
						if tripadvisor_review_item['opinions_user_review'] is None:
							tripadvisor_review_item['opinions_user_review'] = 0

						#========Obtener los votos utilies de usuario  del review -- Actividad
						tripadvisor_review_item['helpful_review'] 		= clean_parsed_string(get_parsed_int(snode_review, './/div[contains(@class,"memberBadging")]/div[contains(@class,"helpfulVotesBadge")]/span/text()'))
						if tripadvisor_review_item['helpful_review'] is None:
							tripadvisor_review_item['helpful_review'] = 0

						#========Guardar el titulo y la descripcion del review de la Actividad
						tripadvisor_item['reviews_actividad'].append(tripadvisor_review_item)
			tripadvisor_item['count_review']  = contador_mensajes

			#Obtener la URL de la pagina siguiente de los review (PAGINACION)
			next_page_url = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next rndBtn ")]/@href'))
			if next_page_url and len(next_page_url) > 0:
				#========Concatenar la URL del titulo de la paginacion de los review
				url_review = self.base_uri + next_page_url
				yield Request(url=url_review, cookies={'store_language':'en'}, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review' : counter_page_review}, callback=self.parse_fetch_review)
			#Si no existe la paginacion siguiente, guardo la paginacion actual
			else:
				yield tripadvisor_item

		# Limites de numero de paginacion
		else:
			yield tripadvisor_item