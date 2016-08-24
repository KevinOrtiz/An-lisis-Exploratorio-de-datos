# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import json
import csv
import string
import unidecode
import json as js
import io


def frecuencia_data(archivo_in, archivo_out):
	#Abro el archivo JSON de los hoteles
	with open(archivo_in) as data_file:
		data_json = json.load(data_file)

	#Creo el archivo CSV
	csv_file = open(archivo_out, 'w')
	#Creo la cabecera del CSV
	cabecera_json = 'Word,Frecuencia\n'
	#Guardo la cabecera en el archivo CSV
	csv_file.write(cabecera_json)

	lista = []
	lista_object = {}
	element_object = {}
	replace_object = {}
	contador = 0
	lista_palabras= []
	for element in data_json:
		lista_reviews = element["reviews"]
		for review in lista_reviews:
			for y, word in enumerate(review):
				palabra, abreviatura = word[0], word[1]

				if palabra in lista_palabras:
					
					for idx, item in enumerate(lista):
							
						if item['palabra'] == palabra:
							#print "lista antes --if:  ",palabra
							#print "",lista
							contador = item['contador'] + 1
							replace_object['palabra'] = palabra
							replace_object['contador'] = contador
							
							#print "lista despues --if\n",lista
							#item = replace_all(item, replaceDictionary)
							lista[idx] = replace_object
							
							replace_object = {}
				else:
					if not (palabra == ',' or 
							palabra == ';' or 
							palabra == ':' or 
							palabra == '.' or 
							palabra == '(' or 
							palabra == ')' or 
							palabra.isdigit() or 
							len(palabra) < 3  or
							'.' in palabra):
						
						lista_palabras.append(palabra)
						#print "lista antes \n",lista
						element_object['palabra'] = palabra
						element_object['contador'] = 1
						
						lista.append(element_object)
						#print "lista despues \n",lista
						element_object = {}
	#print "\n\nLista ",archivo_out,' \n',lista
	for data in lista:
		line = data['palabra']+','+str(data['contador'])+'\n'
		csv_file.write(line)
							

if __name__ == '__main__':
	#frecuencia_data_hotels()
	frecuencia_data('FileTokenizationHotelsGeolocalizedSpanish.text', 'word_frecuencia_data_set_hotels_Spanish.csv')
	frecuencia_data('FileTokenizationHotelsGeolocalizedEnglish.text', 'word_frecuencia_data_set_hotels_English.csv')
	frecuencia_data('FileTokenizationActivitiesGeolocalizedSpanish.text', 'word_frecuencia_data_set_activities_Spanish.csv')
	frecuencia_data('FileTokenizationActivitiesGeolocalizedEnglish.text', 'word_frecuencia_data_set_activities_English.csv')