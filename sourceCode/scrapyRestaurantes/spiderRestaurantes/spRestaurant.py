from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import selector, loader, Request
from ProyectoAnalisis.itemsRestaurantes import itemsRestaurantes
from scrapy.loader import ItemLoader
from crawlerhelper import *


class spRestaurant(CrawlSpider):
		name ="Restaurantes_Trip_Advisor"
		allowed_domains = ['tripadvisor.co']
		start_urls = [
			"https://www.tripadvisor.co/Restaurants-g294308-Quito_Pichincha_Province.html"
		]
		rules = [
			Rule(LinkExtractor(restrict_xpaths=".//div[@id='EATERY_LIST_CONTENTS']//div[@class='pageNumbers']/a"),follow=True),
			Rule(LinkExtractor(restrict_xpaths=".//h3[@class='title']/a"),callback='parseRestaurant',follow=True),
		]

		def parseRestaurant(self,response):

			l= ItemLoader(item=itemsRestaurantes(),response = response)
			l.add_xpath('tituloLugar',".//h1[@id='HEADING']/text()")
			l.add_xpath('tituloComentario',".//div[@class='innerBubble']/div[@class='wrap']//a/span/text()")
			l.add_xpath('latitud',".//div[@id='NEARBY_TAB']/div[@class='content']/div[@class='mapWrap']/div[@class='mapContainer']/@data-lat")
			l.add_xpath('longitud',".//div[@id='NEARBY_TAB']/div[@class='content']/div[@class='mapWrap']/div[@class='mapContainer']/@data-lng")
			l.add_xpath('comentarios',".//div[@class='wrap']/div[@class='entry']/p/text()")
			l.add_xpath('estrellas',".//div[@id='REVIEWS']//div[@class='wrap']//img//@alt")
			yield l.load_item()








	



