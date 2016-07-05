import scrapy as sc
from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor

from scrapy.selector import Selector

from scrapy import loader
from scrapy.loader import ItemLoader
from ProyectoAnalisis.itemsAlquiler import itemsAlquiler

class SpiderRestaurantes(CrawlSpider):
	name = "Alquileres_Quito"
	allowed_domains = ["tripadvisor.co"]
	start_urls = [
		"https://www.tripadvisor.co/VacationRentals-g294308-Reviews-Quito_Pichincha_Province-Vacation_Rentals.html"
	]
	rules = [
	  Rule(LinkExtractor(restrict_xpaths=".//div[@class='pgLinks']//a"), follow=True),
	  Rule(LinkExtractor(restrict_xpaths="//*[@id='REVIEWS']/div[15]/div/div/a[1]"),follow=True),
	  Rule(LinkExtractor(restrict_xpaths=".//div[@class='titleText']//a"),callback='parseAlquiler',follow=True),
	]

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
