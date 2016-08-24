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
	allowed_domains = ["tripadvisor.co"]
	base_uri = "http://www.tripadvisor.co"
	start_urls = [
		base_uri + "/Hotels-g294308-Quito_Pichincha_Province-Hotels.html"
	]


	# Entry point for BaseSpider.
	# Page type: /BuscaCosasQueHacer -- Page type: /Hoteles_Review -- pagination
	def parse(self, response):
		sel = Selector(response)
		#Selector de todos las Hoteles
		snode_hotels = sel.xpath('//div[@id="ACCOM_OVERVIEW"]//div[contains(@class, "listing easyClear")]')
		counter_page_hotels = 0

		#Limitador de paginacion  ==== >>  MAX_REVIEWS_PAGES = 500
		if counter_page_hotels < MAX_REVIEWS_PAGES:
			#Contador de paginacion principal
			counter_page_hotels = counter_page_hotels + 1

			# Iteracion de cada hotel en la pagina semilla
			for snode_hotel in snode_hotels:
				#========Instanciar el item Hotel
				tripadvisor_item = TripAdvisorItem()
				#========Obtener la URL del Hoteles
				url_name_hotel = clean_parsed_string(get_parsed_string(snode_hotel, './/div[contains(@class, "listing_title")]/a/@href'))
				#========Obtener el nombre del Hoteles
				tripadvisor_item['name_hotel'] = clean_parsed_string(get_parsed_string(snode_hotel, './/div[contains(@class, "listing_title")]/a/text()'))
				#========Obtener el numero de opiniones de Hotel
				tripadvisor_item['opinions_hotel'] = clean_parsed_string(get_parsed_int(snode_hotel, './/div[contains(@class ,"listing_info")]/div[contains(@class, "listing_rating")]//span[@class="more"]/a/text()'))
				#========Obtener el rating del Hotel
				tripadvisor_item['rating_hotel'] = clean_parsed_string(get_parsed_int(snode_hotel, './/div[contains(@class, "listing_rating")]/div[@class="rating"]/div/span/img/@alt'))
				
				#========Pregunta si La URL no es None
				if url_name_hotel:
					#========Concatenar la URL del Hotel
					url_name_hotel = self.base_uri + url_name_hotel
					yield Request(url=url_name_hotel, meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page)

			#========Obtener la URL de la pagina siguiente (PAGINACION)
			next_page_hotels = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next ui_button primary taLnk")]/@href'))

			if next_page_hotels and len(next_page_hotels) > 0:
				#========Concatenar la URL de la paginacion de Hoteles
				url_hotels = self.base_uri + next_page_hotels
				yield Request(url=url_hotels, meta={'counter_page_hotels' : counter_page_hotels}, callback=self.parse)


	# Buscar los raiting, ubucacion y los links de los reviews.
	# Page type: /Activiades_Review
	def parse_search_page(self, response):
		#========Obtengo el iten con los datos guardados
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)
		#========Lista el review del Hoteles
		tripadvisor_item['reviews_hotel'] = []
		#========Obtener las coordenadas de posicion del Hotel
		lng = clean_parsed_string(get_parsed_string(sel, '//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lng'))
		lat = clean_parsed_string(get_parsed_string(sel, '//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lat'))


		coordinates = [str(lng), str(lat)]		#Almacena la Longitud y la Latitud del Hoteles y lo guarda en una lista

		#========Pregunta si las coordenadas son NULAS
		if lng  and lat:
			#========Almacena la ubicacion del Hoteles
			tripadvisor_item['location_hotel'] = coordinates

			#========Pregunta si La URL no es None
			url_name_review = clean_parsed_string(get_parsed_string(sel, './/div[@class="quote"]/a/@href'))
			if url_name_review:
				#========Concatenar la URL del titulo del review
				url_review = self.base_uri + url_name_review
				yield Request(url=url_review, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review' : 0}, callback=self.parse_fetch_review)
			#Aunque no tenga Review aun asi guarda registro del Hotel
			else: 
				yield tripadvisor_item


	# Si la pagina encuentra un review, hace su analisis exahustivo.
	# Page type: /ShowUserReviews
	def parse_fetch_review(self, response):
		#========Obtengo el iten con los datos guardados
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
					#========Instanciar el item del review del Hoteles
					tripadvisor_review_item = TripAdvisorReviewItem()
					#========Obtener el titulo del review del Hoteles
					tripadvisor_review_item['title_review'] = clean_parsed_string(get_parsed_string(snode_review, './/div[@class="quote"]/a/span/text()'))
					if tripadvisor_review_item['title_review'] is None:
						tripadvisor_review_item['title_review'] = clean_parsed_string(get_parsed_string(snode_review, './/div[@class="quote"]/text()'))

					#========Obtener la descripcion de un review del Hotel
					tripadvisor_review_item['description_review'] 	= get_parsed_string_multiple(snode_review, './/div[@class="entry"]/p/text()')

					if tripadvisor_review_item['title_review'] and  tripadvisor_review_item['description_review']:
						contador_mensajes = contador_mensajes + 1
						
						#========Obtener el rating de un review del Hotel
						tripadvisor_review_item['rating_review'] 		= clean_parsed_string(get_parsed_int(snode_review, './/div[contains(@class,"rating reviewItemInline")]/span/img/@alt'))
						
						#========Obtener el dia de publicacion de un review del Hotel
						tripadvisor_review_item['date_review'] 			= clean_parsed_string(get_parsed_date(snode_review, './/span[contains(@class,"ratingDate")]/@title'))
						if not tripadvisor_review_item['date_review']:
							tripadvisor_review_item['date_review'] 		= clean_parsed_string(get_parsed_date(snode_review, './/span[contains(@class,"ratingDate")]/text()'))

						#========Obtener la descripcion de un review del Hotel
						tripadvisor_review_item['username_review'] 		= clean_parsed_string(get_parsed_string(snode_review, './/div[@class="username mo"]/span/text()'))
						#========Obtener la ubicacion del usuario  del review -- Hotel
						tripadvisor_review_item['location_review'] 		= clean_parsed_string(get_parsed_string(snode_review, './/div[contains(@class,"member_info")]//div[@class="location"]/text()'))
						
						#========Obtener el numero de opinios del usuario  del review -- Hotel
						tripadvisor_review_item['opinions_user_review'] = clean_parsed_string(get_parsed_int(snode_review, './/div[contains(@class,"memberBadging")]//div[contains(@class,"contributionReviewBadge")]/span/text()'))
						if tripadvisor_review_item['opinions_user_review'] is None:
							tripadvisor_review_item['opinions_user_review'] = 0

						#========Obtener los votos utilies de usuario  del review -- Hotel
						tripadvisor_review_item['helpful_review'] 		= clean_parsed_string(get_parsed_int(snode_review, './/div[contains(@class,"memberBadging")]/div[contains(@class,"helpfulVotesBadge")]/span/text()'))
						if tripadvisor_review_item['helpful_review'] is None:
							tripadvisor_review_item['helpful_review'] = 0

						#========Guardar el titulo y la descripcion del review del Hoteles
						tripadvisor_item['reviews_hotel'].append(tripadvisor_review_item)
			tripadvisor_item['count_review']  = contador_mensajes

			#Obtener la URL de la pagina siguiente de los review (PAGINACION)
			next_page_url = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next rndBtn ")]/@href'))
			if next_page_url and len(next_page_url) > 0:
				#========Concatenar la URL del titulo de la paginacion de los review
				url_review = self.base_uri + next_page_url
				yield Request(url=url_review, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review' : counter_page_review}, callback=self.parse_fetch_review)
			#Si no existe la paginacion siguiente, guardo la paginacion actual
			else:
				yield tripadvisor_item

		# Limites de numero de paginacion
		else:
			yield tripadvisor_item