# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import json
import csv
import string
import unidecode
import json as js
import io

	
"""
Funcion: 		frecuencia_data
Autor: 			Jose Velez Gomez
Descripcion: 	
Estado: 		Terminado
"""
def frecuencia_data(input_file, output_file):
	#Abro el archivo JSON de los hoteles
	with open(input_file) as data_file:
		data_json = json.load(data_file)

	#Creo el archivo CSV
	csv_file = open(output_file, 'w')
	#Creo la cabecera del CSV
	cabecera_json = 'Word,Frecuencia\n'
	#Guardo la cabecera en el archivo CSV
	csv_file.write(cabecera_json)

	lista = []
	lista_object = {}
	element_object = {}
	replace_object = {}
	contador = 0
	lista_abreviatura= []
	for element in data_json:
		lista_reviews = element["reviews"]
		for review in lista_reviews:
			for word in review:
				palabra, abreviatura = word[0], word[1]

				if abreviatura in lista_abreviatura:
					for idx, item in enumerate(lista):
						if item['abreviatura'] == abreviatura:
							contador = item['contador'] + 1
							replace_object['abreviatura'] = abreviatura
							replace_object['contador'] = item['contador'] + 1

							#item = replace_all(item, replaceDictionary)
							lista[idx] = replace_object
							replace_object = {}
				else:
					if not (abreviatura == ',' or abreviatura == ';' or abreviatura == ':' or abreviatura == '.' or abreviatura == '(' or abreviatura == ')'):
						
						lista_abreviatura.append(abreviatura)
						element_object['abreviatura'] = abreviatura
						element_object['contador'] = 1
						
						lista.append(element_object)
						element_object = {}
	print "\n\nLista ",output_file,' \n',lista
	for data in lista:
		line = data['abreviatura']+','+str(data['contador'])+'\n'
		csv_file.write(line)
							

if __name__ == '__main__':
	#frecuencia_data_hotels()
	frecuencia_data('FileTokenizationHotelsGeolocalizedSpanish.text', 'frecuencia_data_set_hotels_Spanish.csv')
	frecuencia_data('FileTokenizationHotelsGeolocalizedEnglish.text', 'frecuencia_data_set_hotels_English.csv')
	frecuencia_data('FileTokenizationActivitiesGeolocalizedSpanish.text', 'frecuencia_data_set_activities_Spanish.csv')
	frecuencia_data('FileTokenizationActivitiesGeolocalizedEnglish.text', 'frecuencia_data_set_activities_English.csv')