# -*- coding: utf-8 -*-
# author: Jose Velez

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import selector, loader
from scrapy_hotel.items import ScrapyItem
import scrapy

class tripAdvisorScrapper(CrawlSpider):
	name = "tripadvisor_hotel"
	allowed_domains = ['tripadvisor.co']
	
	start_urls = ['https://www.tripadvisor.co/Hotels-g294308-Quito_Pichincha_Province-Hotels.html']

	rules = (
		#Rule(LinkExtractor(allow = ''), follow = True),
		Rule(LinkExtractor(allow=['/Hotel_Review-g.*Quito_Pichincha_Province.*'], unique=True), callback='parse_items', follow = True),
	) 

	def parse_items(self, response):
		sel = scrapy.selector.Selector(response)
		pagina_hotel = sel.css('#PAGE')

		l = scrapy.loader.ItemLoader(ScrapyItem(), pagina_hotel)
		item = ScrapyItem()
		l.add_xpath('name','.//h1[@id="HEADING"]/text()')
		l.add_xpath('rating', '//*[@id="HEADING_GROUP"]/div/div[2]/div[1]/div/span/img/@alt')
		lng = pagina_hotel.xpath('//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lng').extract_first()
		lat = pagina_hotel.xpath('//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lat').extract_first()
		pos = [str(lng), str(lat)]		#Almacena la Longitud y la Latitud del hotel y lo guarda en una lista
		l.add_xpath('location',pos)

		#Selector de los REVIEWS
		selector_reviews = sel.css('#REVIEWS .reviewSelector')
		list_review = item.reviewsParser(selector_reviews)
		l.add_value('review',list_review)

		yield l.load_item()
		

	