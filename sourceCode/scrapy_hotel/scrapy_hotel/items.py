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


class TripAdvisorReviewItem(Item):

	date = Field()
	title = Field(
		input_processor = MapCompose(unicode.strip, 
									lambda x: unidecode.unidecode(x),
									lambda y: string.replace(y, '\n', ' '),
									lambda z: z.strip),
		output_processor = Join(),
	)
	description = Field(
		input_processor = MapCompose(unicode.strip, 
									lambda x: unidecode.unidecode(x),
									lambda y: string.replace(y, '\n', ' '),
									lambda z: z.strip),
		output_processor = Join(),
	)

class TripAdvisorItem(Item):

	url = Field()
	name = Field(
		input_processor = MapCompose(unicode.strip, lambda x: unidecode.unidecode(x)),
		output_processor = Join(),
	)
	rating = Field(
		input_processor = MapCompose(unicode.strip, lambda x: x.replace(' de 5 estrellas','')),
		output_processor = Join(),
	)
	location = Field()
	reviews = Field()