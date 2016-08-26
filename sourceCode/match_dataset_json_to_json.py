# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import json
import csv
import string
import unidecode
import json as js
import io

"""
Funcion: 		match_get_data_hotel
Autor: 			Jose Velez Gomez
Descripcion: 	
Estado: 		Terminado
"""
def match_get_data_hotel():
	#Abro el archivo JSON de los hoteles
	with open('scrapy_hotel/scrapy_hotel/spiders/data_set_hotel_co.json') as data_file1:
		data_json1 = json.load(data_file1)

	with open('scrapy_hotel/scrapy_hotel/spiders/data_set_hotel_com.json') as data_file2:
		data_json2 = json.load(data_file2)

	lista = []
	cont =0
	with io.open('match_hotels.json','w',encoding='utf-8') as file_json:

		for element1 in data_json1:
			for x, element2 in enumerate(data_json2):
				if element1["name_hotel"] == element2["name_hotel"]:
					reviews1 = element1['reviews_hotel']
					reviews2 = element2['reviews_hotel']
					reviews = reviews1 + reviews2					#Obtengo los reviews de un hotel
					element1['reviews_hotel'] = reviews1 + reviews2
					cont = cont + 1
					lista.append(element1)
		file_json.write(unicode(js.dumps(lista, ensure_ascii=False)))

"""
Funcion: 		match_get_data_actividades
Autor: 			Jose Velez Gomez
Descripcion: 	
Estado: 		Terminado
"""
def match_get_data_actividades():
	#Abro el archivo JSON de los hoteles
	with open('scrapy_hotel/scrapy_hotel/spiders/data_set_actividades_co.json') as data_file1:
		data_json1 = json.load(data_file1)

	with open('scrapy_hotel/scrapy_hotel/spiders/data_set_actividades_com.json') as data_file2:
		data_json2 = json.load(data_file2)

	lista = []
	cont =0
	with io.open('match_activities.json','w',encoding='utf-8') as file_json:

		for element1 in data_json1:
			for x, element2 in enumerate(data_json2):
				if element1["name_actividad"] == element2["name_actividad"]:
					
					reviews1 = element1['reviews_actividad']
					reviews2 = element2['reviews_actividad']
					reviews = reviews1 + reviews2					#Obtengo los reviews de la Actividad
					element1['reviews_actividad'] = reviews1 + reviews2
					cont = cont + 1
					lista.append(element1)
		file_json.write(unicode(js.dumps(lista, ensure_ascii=False)))
							

if __name__ == '__main__':
	match_get_data_hotel()
	match_get_data_actividades()