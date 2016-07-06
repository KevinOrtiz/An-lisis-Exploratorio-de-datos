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
MAX_REVIEWS_PAGES = 500

class tripAdvisorScrapper(BaseSpider):
	name = "tripadvisor_hotel"
	allowed_domains = ["tripadvisor.co"]
	base_uri = "http://www.tripadvisor.co"
	start_urls = [
		base_uri + "/Hotels-g294308-Quito_Pichincha_Province-Hotels.html"
	]


	# Entry point for BaseSpider.
	# Page type: /BuscaCosasQueHacer
	def parse(self, response):
		sel = Selector(response)
		#Selector de todos las Hoteles
		snode_hotels = sel.xpath('//div[@id="ACCOM_OVERVIEW"]//div[starts-with(@class, "property_details easyClear")]')
		
		# Iteracion de cada hotel en la pagina semilla
		for snode_hotel in snode_hotels:
			#========Instanciar el item Hoteles
			tripadvisor_item = TripAdvisorItem()
			#========Obtener la URL del Hoteles
			url_name = clean_parsed_string(get_parsed_string(snode_hotel, './/div[contains(@class, "listing_title")]/a[@class="property_title "]/@href'))
			#========Obtener el nombre del Hoteles
			tripadvisor_item['name'] = clean_parsed_string(get_parsed_string(snode_hotel, './/div[contains(@class, "listing_title")]/a[@class="property_title "]/text()'))

			if url_name:
				#========Concatenar la URL del Hoteles
				url_name = self.base_uri + url_name
				yield Request(url=url_name, meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page)

		#Obtener la URL de la pagina siguiente (PAGINACION)
		next_page_hotels = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next ui_button primary taLnk")]/@href'))

		if next_page_hotels and len(next_page_hotels) > 0:
			#========Concatenar la URL de la paginacion de Hoteles
			url_hotels = self.base_uri + next_page_hotels
			yield Request(url=url_hotels, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_hotels' : 0}, callback=self.parse_pagination)


	#Funcion que obtiene los elementos del review
	# Page type: /Hoteles_Review -- pagination
	def parse_pagination(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)
		#  Contador de las paginas de las Hoteles
		counter_page_hotels = response.meta['counter_page_hotels']
		#  Limite maximo de reviews de las paginas para crawling
		if counter_page_hotels < MAX_REVIEWS_PAGES:
			counter_page_hotels = counter_page_hotels + 1

			#Selector de todas las Hoteles
			snode_hotels = sel.xpath('//div[@id="ACCOM_OVERVIEW"]//div[starts-with(@class, "property_details easyClear")]')
			# Iteracion de cada Hoteles en la pagina semilla
			for snode_hotel in snode_hotels:
				#========Instanciar el item Hoteles
				tripadvisor_item = TripAdvisorItem()
				#========Obtener la URL del Hoteles
				url_name = clean_parsed_string(get_parsed_string(snode_hotel, './/div[contains(@class, "listing_title")]/a[@class="property_title "]/@href'))
				#========Obtener el nombre del Hoteles
				tripadvisor_item['name'] = clean_parsed_string(get_parsed_string(snode_hotel, './/div[contains(@class, "listing_title")]/a[@class="property_title "]/text()'))

				if url_name:
					#========Concatenar la URL del Hoteles
					url_name = self.base_uri + url_name
					yield Request(url=url_name, meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page)
			
			#Obtener la URL de la pagina siguiente (PAGINACION)
			next_page_hotels = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next ui_button primary taLnk")]/@href'))

			if next_page_hotels and len(next_page_hotels) > 0:
				#========Concatenar la URL de la paginacion de Hoteles
				url_hotels = self.base_uri + next_page_hotels
				yield Request(url=url_hotels, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_hotels' : counter_page_hotels}, callback=self.parse_pagination)


	# Buscar los raiting, ubucacion y los links de los reviews.
	# Page type: /Activiades_Review
	def parse_search_page(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)
		#========Lista el review del Hoteles
		tripadvisor_item['reviews'] = []
		#========Obtener el raiting del Hoteles
		tripadvisor_item['rating'] = clean_parsed_string(get_parsed_raiting(sel, '//*[@id="HEADING_GROUP"]/div/div[2]/div[1]/div/span/img/@alt'))
		lng = clean_parsed_string(get_parsed_string(sel, '//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lng'))
		lat = clean_parsed_string(get_parsed_string(sel, '//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lat'))
		if lng is None and lat is None:
			pos = [lng, lat]
		else:  
			pos = [str(lng), str(lat)]		#Almacena la Longitud y la Latitud del Hoteles y lo guarda en una lista
		#========Obtener la ubicacion del Hoteles
		tripadvisor_item['location'] = pos

		expanded_review_url = clean_parsed_string(get_parsed_string(sel, '//div[contains(@class, "basic_review")]//a/@href'))
		if expanded_review_url:
			#========Concatenar la URL del titulo del review
			url_review = self.base_uri + expanded_review_url
			yield Request(url=url_review, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review' : 0}, callback=self.parse_fetch_review)
		#Aunque no tenga Review aun asi guarda registro del Hotel
		else: 
			yield tripadvisor_item


	# Si la pagina encuentra un review, hace su analisis exahustivo.
	# Page type: /ShowUserReviews
	def parse_fetch_review(self, response):
		tripadvisor_item = response.meta['tripadvisor_item']
		sel = Selector(response)
		#  Contador de las paginas de las Hoteles
		counter_page_review = response.meta['counter_page_review']
		# Limite maximo de reviews de las paginas para crawling.
		if counter_page_review < MAX_REVIEWS_PAGES:
			counter_page_review = counter_page_review + 1

			# TripAdvisor reviews for item.
			snode_reviews = sel.xpath('//div[@id="REVIEWS"]/div/div[contains(@class, "review")]/div[@class="col2of2"]/div[@class="innerBubble"]')

			# Reviews for item.
			for snode_review in snode_reviews:
				#========Instanciar el item del review del Hoteles
				tripadvisor_review_item = TripAdvisorReviewItem()
				#========Obtener el titulo del review del Hoteles
				tripadvisor_review_item['title'] = clean_parsed_string(get_parsed_string(snode_review, 'div[@class="quote"]/text()'))
				if tripadvisor_review_item['title'] is None:
					tripadvisor_review_item['title'] = clean_parsed_string(get_parsed_string(snode_review, 'div[@class="quote"]/a/span/text()'))
				
				#========Obtener la descripcion del review del Hoteles
				tripadvisor_review_item['description'] = get_parsed_string_multiple(snode_review, 'div[@class="entry"]/p/text()')
				#========Guardar el titulo y la descripcion del review del Hoteles
				tripadvisor_item['reviews'].append(tripadvisor_review_item)

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