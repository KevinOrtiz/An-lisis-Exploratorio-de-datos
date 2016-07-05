# -*- encoding: utf-8 -*-
# author: Jose Velez
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
MAX_REVIEWS_PAGES = 50

class tripAdvisorScrapper(BaseSpider):
	name = "tripadvisor_hotel"
	allowed_domains = ["tripadvisor.co"]
	base_uri = "http://www.tripadvisor.co"
	start_urls = [
		base_uri + "/Attractions-g294308-Activities-Quito_Pichincha_Province.html"
	]


	# Entry point for BaseSpider.
	# Page type: /BuscaCosasQueHacer
	def parse(self, response):
		sel = Selector(response)
		#Selector de todos las Actividades
		snode_cosas_que_hacers = sel.xpath('//div[@id="FILTERED_LIST"]//div[starts-with(@class, "entry")]')
		
		# Iteracion de cada actividad en la pagina semilla
		for snode_cosas_que_hacer in snode_cosas_que_hacers:
			#========Instanciar el item Actividades
			tripadvisor_item = TripAdvisorItem()
			#========Obtener la URL del Actividades
			url_name = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './/div[contains(@class, "property_title")]/a/@href'))
			#========Obtener el nombre del Actividades
			tripadvisor_item['name'] = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './/div[contains(@class, "property_title")]/a/text()'))

			if url_name:
				#========Concatenar la URL del Actividades
				url_name = self.base_uri + url_name
				yield Request(url=url_name, meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page)

		#Obtener la URL de la pagina siguiente (PAGINACION)
		next_page_actividades = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next rndBtn ui_button primary taLnk")]/@href'))

		if next_page_actividades and len(next_page_actividades) > 0:
			#========Concatenar la URL de la paginacion de Actividades
			url_actividades = self.base_uri + next_page_actividades
			yield Request(url=url_actividades, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_actividades' : 0}, callback=self.parse_pagination)


	#Funcion que obtiene los elementos del review
	# Page type: /Actividades_Review -- pagination
	def parse_pagination(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)
		#  Contador de las paginas de las Actividades
		counter_page_actividades = response.meta['counter_page_actividades']
		#  Limite maximo de reviews de las paginas para crawling
		if counter_page_actividades < MAX_REVIEWS_PAGES:
			counter_page_actividades = counter_page_actividades + 1

			#Selector de todas las Actividades
			snode_cosas_que_hacers = sel.xpath('//div[@id="FILTERED_LIST"]//div[starts-with(@class, "entry")]')
			
			# Iteracion de cada Actividades en la pagina semilla
			for snode_cosas_que_hacer in snode_cosas_que_hacers:
				#========Instanciar el item Actividades
				tripadvisor_item = TripAdvisorItem()
				#========Obtener la URL del Actividades
				url_name = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './/div[contains(@class, "property_title")]/a/@href'))
				#========Obtener el nombre del Actividades
				tripadvisor_item['name'] = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './/div[contains(@class, "property_title")]/a/text()'))

				if url_name:
					#========Concatenar la URL del Actividades
					url_name = self.base_uri + url_name
					yield Request(url=url_name, meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page)
			
			#Obtener la URL de la pagina siguiente (PAGINACION)
			next_page_actividades = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next rndBtn ui_button primary taLnk")]/@href'))

			if next_page_actividades and len(next_page_actividades) > 0:
				#========Concatenar la URL de la paginacion de Actividades
				url_actividades = self.base_uri + next_page_actividades
				yield Request(url=url_actividades, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_actividades' : counter_page_actividades}, callback=self.parse_pagination)


	# Buscar los raiting, ubucacion y los links de los reviews.
	# Page type: /Activiades_Review
	def parse_search_page(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)
		#========Lista el review del Actividades
		tripadvisor_item['reviews'] = []
		#========Obtener el raiting del Actividades
		tripadvisor_item['rating'] = clean_parsed_string(get_parsed_string(sel, '//*[@id="HEADING_GROUP"]/div/div[2]/div[1]/div/span/img/@alt'))
		lng = clean_parsed_string(get_parsed_string(sel, '//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lng'))
		lat = clean_parsed_string(get_parsed_string(sel, '//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lat'))
		pos = [str(lng), str(lat)]		#Almacena la Longitud y la Latitud del Actividades y lo guarda en una lista
		#========Obtener la ubicacion del Actividades
		tripadvisor_item['location'] = pos

		expanded_review_url = clean_parsed_string(get_parsed_string(sel, '//div[contains(@class, "basic_review")]//a/@href'))
		if expanded_review_url:
			#========Concatenar la URL del titulo del review
			url_review = self.base_uri + expanded_review_url
			yield Request(url=url_review, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review' : 0}, callback=self.parse_fetch_review)


	# Si la pagina encuentra un review, hace su analisis exahustivo.
	# Page type: /ShowUserReviews
	def parse_fetch_review(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)
		#  Contador de las paginas de las Actividades
		counter_page_review = response.meta['counter_page_review']
		# Limite maximo de reviews de las paginas para crawling.
		if counter_page_review < MAX_REVIEWS_PAGES:
			counter_page_review = counter_page_review + 1

			# TripAdvisor reviews for item.
			snode_reviews = sel.xpath('//div[@id="REVIEWS"]/div/div[contains(@class, "review")]/div[@class="col2of2"]/div[@class="innerBubble"]')

			# Reviews for item.
			for snode_review in snode_reviews:
				#========Instanciar el item del review del Actividades
				tripadvisor_review_item = TripAdvisorReviewItem()
				#========Obtener el titulo del review del Actividades
				tripadvisor_review_item['title'] = clean_parsed_string(get_parsed_string(snode_review, 'div[@class="quote"]/text()'))
				if tripadvisor_review_item['title'] is None:
					tripadvisor_review_item['title'] = clean_parsed_string(get_parsed_string(snode_review, 'div[@class="quote"]/a/span/text()'))
				#========Obtener la descripcion del review del Actividades
				tripadvisor_review_item['description'] = get_parsed_string_multiple(snode_review, 'div[@class="entry"]/p/text()')
				#========Guardar el titulo y la descripcion del review del Actividades
				tripadvisor_item['reviews'].append(tripadvisor_review_item)

			#Obtener la URL de la pagina siguiente de los review (PAGINACION)
			next_page_url = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next rndBtn ")]/@href'))
			if next_page_url and len(next_page_url) > 0:
				#========Concatenar la URL del titulo de la paginacion de los review
				url_review = self.base_uri + next_page_url
				yield Request(url=url_review, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review' : counter_page_review}, callback=self.parse_fetch_review)
			else:
				yield tripadvisor_item

		# Limites de numero de paginacion
		else:
			yield tripadvisor_item