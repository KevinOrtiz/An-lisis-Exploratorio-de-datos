# -*- coding: utf-8 -*-
# author: Jose Velez

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import selector, loader, Request
from scrapy_hotel.items import ScrapyItem, TripAdvisorReviewItem
from crawlerhelper import *
import scrapy
import re
import time

MAX_REVIEWS_PAGES = 500

class tripAdvisorScrapper(CrawlSpider):
	name = "tripadvisor_hotel"
	allowed_domains = ['tripadvisor.co']
	base_uri = 'https://www.tripadvisor.co'
	start_urls = ['https://www.tripadvisor.co/Hotels-g294308-Quito_Pichincha_Province-Hotels.html']

	rules = (
		#Rule(LinkExtractor(allow = ''), follow = True),
		Rule(LinkExtractor(allow=['/Hotel_Review-g.*Quito_Pichincha_Province.*'], unique=True), callback='parse_items', follow = True),
	) 

	def parse_items(self, response):
		sel = scrapy.selector.Selector(response)
		pagina_hotel = sel.css('#PAGE')

		l = scrapy.loader.ItemLoader(ScrapyItem(), pagina_hotel)
		l.add_xpath('name','.//h1[@id="HEADING"]/text()')
		l.add_xpath('rating', '//*[@id="HEADING_GROUP"]/div/div[2]/div[1]/div/span/img/@alt')
		lng = pagina_hotel.xpath('//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lng').extract_first()
		lat = pagina_hotel.xpath('//*[@id="NEARBY_TAB"]/div/div[1]/div[3]/@data-lat').extract_first()
		pos = [str(lng), str(lat)]		#Almacena la Longitud y la Latitud del hotel y lo guarda en una lista
		l.add_xpath('location',pos)
		list_review = []
		l.add_value('review', list_review)

		# The default page contains the reviews but the reviews are shrink and need to click 'More' to view the complete content.
		# An alternate way is to click one of the reviews in the page to open the expanded reviews display page.
		# We're using this last solution to avoid AJAX here.
		expanded_review_url = clean_parsed_string(get_parsed_string(sel, '//div[contains(@class, "basic_review")]//a/@href'))
		if expanded_review_url:
			yield Request(url=self.base_uri + expanded_review_url, meta={'hotel_item': l, 'counter_page_review' : 0}, callback=self.parse_fetch_review)

		# #Selector de los REVIEWS
		# selector_reviews = sel.css('#REVIEWS .reviewSelector')
		# list_review = item.reviewsParser(selector_reviews)
		# l.add_value('review',list_review)

		# yield l.load_item()


	def parse_fetch_review(self, response):
		hotel_item = response.meta['hotel_item']
		sel = scrapy.selector.Selector(response)

		counter_page_review = response.meta['counter_page_review']

		# Limit max reviews pages to crawl.
		if counter_page_review < MAX_REVIEWS_PAGES:
			counter_page_review = counter_page_review + 1

			# TripAdvisor reviews for item.
			snode_reviews = sel.xpath('//div[@id="REVIEWS"]/div/div[contains(@class, "review")]/div[@class="col2of2"]/div[@class="innerBubble"]')

			# Reviews for item.
			for snode_review in snode_reviews:
				tripadvisor_review_item = TripAdvisorReviewItem()

				tripadvisor_review_item['title'] = clean_parsed_string(get_parsed_string(snode_review, 'div[@class="quote"]/text()'))

				# Review item description is a list of strings.
				# Strings in list are generated parsing user intentional newline. DOM: <br>
				tripadvisor_review_item['description'] = get_parsed_string_multiple(snode_review, 'div[@class="entry"]/p/text()')
				# Cleaning string and taking only the first part before whitespace.
				snode_review_item_stars = clean_parsed_string(get_parsed_string(snode_review, 'div[@class="rating reviewItemInline"]/span[starts-with(@class, "rate")]/img/@alt'))
				tripadvisor_review_item['stars'] = re.match(r'(\S+)', snode_review_item_stars).group()

				snode_review_item_date = clean_parsed_string(get_parsed_string(snode_review, 'div[@class="rating reviewItemInline"]/span[@class="ratingDate"]/text()'))
				snode_review_item_date = re.sub(r'Reviewed ', '', snode_review_item_date, flags=re.IGNORECASE)
				snode_review_item_date = time.strptime(snode_review_item_date, '%B %d, %Y') if snode_review_item_date else None
				tripadvisor_review_item['date'] = time.strftime('%Y-%m-%d', snode_review_item_date) if snode_review_item_date else None

				hotel_item.get_collected_values('review').append(tripadvisor_review_item)


			# Find the next page link if available and go on.
			next_page_url = clean_parsed_string(get_parsed_string(sel, '//a[starts-with(@class, "guiArw sprite-pageNext ")]/@href'))
			if next_page_url and len(next_page_url) > 0:
				yield Request(url=self.base_uri + next_page_url, meta={'hotel_item': hotel_item, 'counter_page_review' : counter_page_review}, callback=self.parse_fetch_review)
			else:
				yield hotel_item.load_item()

		# Limitatore numero di pagine di review da passare. Totale review circa 5*N.
		else:
			yield hotel_item.load_item()
		

	