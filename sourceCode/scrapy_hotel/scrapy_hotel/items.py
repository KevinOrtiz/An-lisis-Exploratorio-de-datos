# -*- coding: utf-8 -*-
__author__ = 'josanvel'

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.item import Item, Field
import unidecode
import string

class TripAdvisorReviewItem(Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	title_review = Field()
	rating_review = Field()
	date_review = Field()
	username_review = Field()
	location_review = Field()
	opinions_user_review = Field()
	helpful_review = Field()
	description_review = Field()


class TripAdvisorItem(Item):
	# define the fields for your item here like:

	name_hotel = Field()
	opinions_hotel =Field()
	rating_hotel = Field()
	location_hotel = Field()
	reviews_hotel = Field()


class TripAdvisorItemCosasHacer(Item):
	# define the fields for your item here like:

	name_actividad = Field()
	opinions_actividad =Field()
	rating_actividad = Field()
	location_actividad = Field()
	reviews_actividad = Field()
	tags_categorias_actividades = Field()