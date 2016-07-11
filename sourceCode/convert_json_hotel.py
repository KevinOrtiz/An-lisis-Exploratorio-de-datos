# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import json
import csv
import string
import unidecode

def get_fields_json(name_file):
	#Abro el archivo JSON de los hoteles
	with open(name_file) as data_file:
		data_json = json.load(data_file)

	#Creo el archivo CSV
	csv_file = open('../data/TripAdvisor/pdata_final_hotel_co.csv', 'w')
	#Creo la cabecera del CSV
	cabecera_json = 'NAME,USER,LONGITUDE,LATITUDE,RATING,NoREVIEWS,HELPFUL,NoOpinionsHotels,CITY,COUNTRY\n'
	#Guardo la cabecera en el archivo CSV
	csv_file.write(cabecera_json)

	for element in data_json:
		#Obtengo la ubicacion del Hotel en cooredenadas
		location = element['location']
		lng = location[0]
		lat = location[1]
		
		if not (lng is None and lat is None):

			#===========Verifica que el registro tengo RATING
			rating = element['rating']					#Obtengo el raiting de la Actividad
			if rating:
				name = element['name']					#Obtengo el nombre de un hotel
				name = string.replace(name, ',', '')	
				reviews = element['reviews']			#Obtengo los reviews de un hotel
				NoReviews = len(reviews)				#Obtengo el numoero de reviews de un hotel

				if NoReviews > 0:
					for review in reviews:
						user = review['user_review']
						if user:
							location_user = review['location_review']
							if location_user:
								helpful = review['votes_helpful']
								if helpful:
									opinions = review['opinions_review']
									location_user = unidecode.unidecode(location_user)
									location_user = location_user.split(', ')

									if len(location_user) > 2:
										country = location_user[2]
										city = location_user[0]+' '+location_user[1]
									elif len(location_user) == 2:
										city = location_user[0]
										country = location_user[1]
									else:
										city = location_user[0]
										country = city

									#Concateno la linea del CSV
									line = str(name)+','+str(user)+','+str(lng)+','+str(lat)+','+str(rating)+','+str(NoReviews)+','+str(helpful)+','+str(opinions)+','+str(city)+','+str(country)+'\n'
									#Guardo la linea en el archivo CSV
									csv_file.write(line)

if __name__ == '__main__':
	get_fields_json('scrapy_hotel/scrapy_hotel/spiders/hotel_data_co.json')
