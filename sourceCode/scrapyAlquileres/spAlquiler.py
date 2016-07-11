import scrapy as sc
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy import loader
from scrapy.loader import ItemLoader
from crawlerhelper import *
from itemsAlquiler import *
from scrapy.conf import settings
MAX_REVIEWS_PAGES = 500

# Constants.
# Max reviews pages to crawl.
# Reviews collected are around: 5 * MAX_REVIEWS_PAGES


class tripAdvisorScrapper(BaseSpider):
	name = "tripadvisor_restaurant"
	allowed_domains = ["tripadvisor.com","tripadvisor.co"]
	base_uri = "http://www.tripadvisor.co"
	start_urls = [
		"https://www.tripadvisor.com/VacationRentalReview-g294308-d1905978-Peaceful_Garden_Suites_Luna_in_Historical_Quito-Quito_Pichincha_Province.html#REVIEWS",
		"https://www.tripadvisor.co/VacationRentalReview-g294308-d1905978-or12-Peaceful_Garden_Suites_Luna_in_Historical_Quito-Quito_Pichincha_Province.html#REVIEWS"
	]


	# Entry point for BaseSpider.
	# Page type: /BuscaCosasQueHacer
	def parse(self, response):
		sel = Selector(response)
		#Selector de todos las Actividades
		snode_reviews = sel.xpath('.//div[@id="REVIEWS"]//div[contains(@class,"reviewSelector ")]')
		print snode_reviews
		cont = 0
		tripadvisor_review_item = itemsReviews()


		# Iteracion de cada actividad en la pagina semilla
		for snode_review in snode_reviews:
			#========Instanciar el item Actividades
			#print snode_review
			#========Obtener la URL del Actividades
			tripadvisor_review_item['tituloComentario'] = clean_parsed_string(get_parsed_string(snode_review, './/div[@class="quote"]/text()'))

			if tripadvisor_review_item['tituloComentario'] is None:
				tripadvisor_review_item['tituloComentario'] = clean_parsed_string(get_parsed_string(snode_review, './/div[@class="quote"]/a/span/text()'))
			
			print "Titulo del revews:", tripadvisor_review_item['tituloComentario']
			
			#========Obtener la descripcion del review del Hoteles
			tripadvisor_review_item['comentarios'] = get_parsed_string_multiple(snode_review, './/div[@class="entry"]/p/text()')

			if tripadvisor_review_item['comentarios'] is None:
				tripadvisor_review_item['comentarios'] = get_parsed_string_multiple(snode_review, './/div[@class="innerBubble"]//div[contains(@class,"vrReviewText")]//span/text()')

			print tripadvisor_review_item['comentarios']

			#========Guardar el titulo y la descripcion del review del Hoteles
			#tripadvisor_item['reviews'].append(tripadvisor_review_item)
			print "Contador: ",cont
			cont = cont + 1

			yield tripadvisor_review_item