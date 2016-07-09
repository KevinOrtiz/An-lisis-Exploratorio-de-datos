# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import json
import csv
import string

def get_fields_json():
	#Abro el archivo JSON de los hoteles
	with open('scrapy_hotel/scrapy_hotel/spiders/data_hotel.json') as data_file:
		data_json = json.load(data_file)

	#Creo el archivo CSV
	csv_file = open('../data/TripAdvisor/nuevo_data_hotel.csv', 'w')
	#Creo la cabecera del CSV
	cabecera_json = 'name,longitude,latitude,rating,NoReviews\n'
	#Guardo la cabecera en el archivo CSV
	csv_file.write(cabecera_json)

	for element in data_json:
		#Obtengo la ubicacion del Hotel en cooredenadas
		location = element['location']
		lng = location[0]
		lat = location[1]
		
		if not (lng is None and lat is None):
			name = element['name']					#Obtengo el nombre de un hotel
			name = string.replace(name, ',', '')	
			rating = element['rating']				#Obtengo el raiting de un hotel
			reviews = element['reviews']			#Obtengo los reviews de un hotel
			NoReviews = len(reviews)				#Obtengo el numoero de reviews de un hotel

			#Concateno la linea del CSV
			line = str(name)+','+str(lng)+','+str(lat)+','+str(rating)+','+str(NoReviews)+'\n'
			#Guardo la linea en el archivo CSV
			if rating:
				csv_file.write(line)

if __name__ == '__main__':
	get_fields_json()