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
MAX_REVIEWS_PAGES = 500


class SpiderAlquiler(BaseSpider):
	name = "tripadvisor_Alquiler"
	allowed_domains = ["tripadvisor.co","tripadvisor.com","fr.tripadvisor.ca","tripadvisor.de"]
	base_uri = "http://www.tripadvisor.co"
	start_urls = [
		base_uri + "/VacationRentals-g294308-Reviews-Quito_Pichincha_Province-Vacation_Rentals.html"
		"https://www.tripadvisor.com/VacationRentals-g294308-Reviews-Quito_Pichincha_Province-Vacation_Rentals.html"
		"https://fr.tripadvisor.ca/VacationRentals-g294308-Reviews-Quito_Pichincha_Province-Vacation_Rentals.html"
		"https://www.tripadvisor.de/VacationRentals-g294308-Reviews-Quito_Pichincha_Province-Vacation_Rentals.html"
	]


	# Entry point for BaseSpider.
	# Page type: /BuscaCosasQueHacer
	def parse(self, response):
		sel = Selector(response)
		#Selector de todos las Actividades
		snode_cosas_que_hacers = sel.xpath('//div[@id="ACCOM_OVERVIEW"]//div[starts-with(@class, "twoColListing")]')

		# Iteracion de cada actividad en la pagina semilla
		for snode_cosas_que_hacer in snode_cosas_que_hacers:
			#========Instanciar el item Actividades
			tripadvisor_item = itemsAlquiler()
			#========Obtener la URL del Actividades
			url_name = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './/div[contains(@class, "titleText")]/a/@href'))
			#========Obtener el nombre del Actividades
			tripadvisor_item['tituloLugar'] = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './/div[contains(@class, "titleText")]/a/span/text()'))
			
			if url_name:
				#========Concatenar la URL del Actividades
				url_name = self.base_uri + url_name
				yield Request(url=url_name, meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page)
			
		#Obtener la URL de la pagina siguiente (PAGINACION)
		next_page_actividades = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "vrPagingLink nextArrow")]/@href'))

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
			snode_cosas_que_hacers = sel.xpath('//div[@id="ACCOM_OVERVIEW"]//div[starts-with(@class, "twoColListing")]')
			# Iteracion de cada Actividades en la pagina semilla
			for snode_cosas_que_hacer in snode_cosas_que_hacers:
				#========Instanciar el item Actividades
				tripadvisor_item = itemsAlquiler()
				#========Obtener la URL del Actividades
				url_name = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './/div[contains(@class, "titleText")]/a/@href'))
				#========Obtener el nombre del Actividades
				tripadvisor_item['tituloLugar'] = clean_parsed_string(get_parsed_string(snode_cosas_que_hacer, './/div[contains(@class, "titleText")]/a/span/text()'))
				
				if url_name:
					#========Concatenar la URL del Actividades
					url_name = self.base_uri + url_name
					yield Request(url=url_name, meta={'tripadvisor_item': tripadvisor_item}, callback=self.parse_search_page)
				
			#Obtener la URL de la pagina siguiente (PAGINACION)
			next_page_actividades = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "vrPagingLink nextArrow")]/@href'))

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
		tripadvisor_item['itemsReviews'] = []
		#========Obtener el raiting del Actividades
		tripadvisor_item['estrellas'] = clean_parsed_string(get_parsed_rating(sel, ".//div[@id='REVIEWS']//div[@class='wrap']//img/@alt"))
		tripadvisor_item['precio'] = clean_parsed_string(get_parsed_rating(sel, "//span[@id='fromDailyRate']/text()"))
		lng = clean_parsed_string(get_parsed_string(sel, ".//div[@id='NEARBY_TAB']/div[@class='content']/div[@class='mapWrap']/div[@class='mapContainer']/@data-lng"))
		lat = clean_parsed_string(get_parsed_string(sel, ".//div[@id='NEARBY_TAB']/div[@class='content']/div[@class='mapWrap']/div[@class='mapContainer']/@data-lat"))
		if lng is None and lat is None:
			pos = [lng, lat]
		else:  
			pos = [str(lng), str(lat)]		#Almacena la Longitud y la Latitud del Actividades y lo guarda en una lista
		#========Obtener la ubicacion del Actividades
		tripadvisor_item['posicion'] = pos

		#========Obtengo el selector de tags
		tags = sel.xpath("//*[@id='REVIEWS']//span[@class='rate']//span[@class='rating-in-language']/text()")
		#========Obtener los tags de Actividades
		tripadvisor_item['categoria'] = tags

		expanded_review_url = clean_parsed_string(get_parsed_string(sel, "//div[@class='innerBubble']//div[@class='wrap']/div[@class='quote']/a/@href"))
		if expanded_review_url:
			#========Concatenar la URL del titulo del review
			url_review = self.base_uri + expanded_review_url
			yield Request(url=url_review, meta={'tripadvisor_item': tripadvisor_item, 'counter_page_review' : 0}, callback=self.parse_fetch_review)
		#Aunque no tenga Review aun asi se guarda registro de la Actividad
		else: 
			yield tripadvisor_item


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
			snode_reviews = sel.xpath('//div[@class="deckB review_collection "]//div[@class="vrrmReviewScroller"]//div[@class="col2of2"]/div[@class="innerBubble"]')

			# Reviews for item.
			print snode_reviews
			tripadvisor_review_item = itemsReviews()
			for snode_review in snode_reviews:
				#========Instanciar el item del review del Actividades
				
				#========Obtener el titulo del review del Actividades
				tripadvisor_review_item['tituloComentario'] = clean_parsed_string(get_parsed_string(snode_review,".//div[@class='wrap']//div[@class='quote']/a/text()"))
				#========Obtener la descripcion del review del Actividades
				tripadvisor_review_item['comentarios'] = get_parsed_string_multiple(snode_review, ".//div[@class='summary']//p/span/text()")
				#========Guardar el titulo y la descripcion del review del Actividades
				tripadvisor_item['itemsReviews'].append(tripadvisor_review_item)

			#Obtener la URL de la pagina siguiente de los review (PAGINACION)
			next_page_url = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "nav next rndBtn ui_button primary taLnk")]/@href'))
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

	




	'''

	def parseAlquiler(self,response):
		 l= ItemLoader(item=itemsAlquiler(),response = response)
		 l.add_xpath('tituloLugar',".//h1[@id='HEADING']/text()")
		 l.add_xpath('tituloComentario',".//div[@id='REVIEWS']//div[@class='wrap']//div[@class='quote']//a/text()")
		 l.add_xpath('latitud',".//div[@id='NEARBY_TAB']/div[@class='content']/div[@class='mapWrap']/div[@class='mapContainer']/@data-lat")
		 l.add_xpath('longitud',".//div[@id='NEARBY_TAB']/div[@class='content']/div[@class='mapWrap']/div[@class='mapContainer']/@data-lng")
		 l.add_xpath('comentarios',"//div[@id='reviewsCard']//div[@class='wrap']//div[@class='summary']//p[@class='partial_entry']//text()")
		 l.add_xpath('estrellas',".//div[@id='REVIEWS']//div[@class='wrap']//img//@alt")
		 l.add_xpath('precio',"//span[@id='fromDailyRate']/text()")
		 yield l.load_item()
	'''