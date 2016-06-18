# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.item import Item, Field
import unidecode
import string


class ScrapyItem(Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	
	name = scrapy.Field(
		input_processor = MapCompose(unicode.strip, lambda x: unidecode.unidecode(x)),
		output_processor = Join(),
	)
	rating = Field(
		input_processor = MapCompose(unicode.strip, lambda x: x.replace(' de 5 estrellas','')),
		output_processor = Join(),
	)
	location = Field()
	review = Field()
	

	def reviewsParser(self, selector):
		listaReviews = []

		for i, elem in enumerate(selector):
			#Primera estructura del contenido del review
			review = elem.xpath('.//p[@class="partial_entry"]/text()').extract_first()
			
			if review:
				review = review.strip()
				review = unidecode.unidecode(review)
				review = string.replace(review, '\n', ' ')
				#Almacena en la lista el reiview de la primera estructura
				listaReviews.append(review)
			else:
				#Segunda estructura del contenido del review
				review = elem.xpath('.//p[@class="partial_entry"]/span[1]/text()').extract_first()

				if review:
					review = review.strip()
					review = unidecode.unidecode(review)
					review = string.replace(review, '\n', ' ')
					#Almacena en la lista el reiview de la segunda estructura
					listaReviews.append(review)

		return listaReviews