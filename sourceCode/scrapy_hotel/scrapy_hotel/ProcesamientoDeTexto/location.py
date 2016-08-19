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
list_dict_positivo = ['bueno', 'positivo', 'suerte', 'correcto', 'superior', 'atractivo', 'impresionante', 'fantastico', 'favorito','divertido','alegre', 'grande', 'feliz','amor', 'perfecto', 'satisfecho','valor', 'excelente', 'amable', 'cerca', 'comodo', 'agradable', 'recomendar', 'encanto', 'mejor','confortable', 'espectacular', 'amabilidad', 'bonito', 'amplio', 'limpio', 'descansar', 'gracias', 'seguro', 'relajante', 'maravilloso', 'lujoso', 'elegante', 'disponible', 'acceder']
list_dict_neutral = ['super', 'detalle', 'bastante', 'precio', 'calidad', 'ubicado', 'dias', 'todas', 'cuenta','estadia', 'restaurante', 'sector', 'ambiente', 'experiencia', 'variado', 'economico', 'costoso', 'gratis']
list_dict_negativo = ['malo', 'pobre',  'lamentable',  'inferior', 'molesto','odio', 'basura', 'suciedad','arrepentimiento', 'perdon', 'terrible', 'inaceptable', 'peor','decepcionado', 'antiguo', 'mejorar', 'salir', 'riesgo', 'quejas', 'problemas', 'pestilente', 'perder', 'necesidad', 'mediocre', 'lejos', 'incidentes', 'humo', 'sucio', 'desagradable', 'ruido', 'demora', 'negativo']

def frecuencia_data_location(input_file, output_file1,output_file2,output_file3,ubicacion):
	#Abro el archivo JSON de los hoteles
	with open(input_file) as data_file:
		data_json = json.load(data_file)

	lista_object = {}
	element_object = {}
	replace_object = {}
	contador = 0
	lista_positiva = []
	lista_negativa = []
	lista_neutral = []


	with io.open(output_file1,'w',encoding='utf-8') as data_loactiom_frequency_positivo:
		with io.open(output_file2,'w',encoding='utf-8') as data_loactiom_frequency_negativo:
			with io.open(output_file3,'w',encoding='utf-8') as data_loactiom_frequency_neutral:
				for element in data_json:
					location = element[ubicacion]

					if location[0] is not None and location[1] is not None:
						lista_reviews = element["reviews"]
						lista_palabras= []
						lista_words = []

						if lista_reviews:

							for review in lista_reviews:

								for y, word in enumerate(review):
									palabra, abreviatura = word[0].lower(), word[1]


									if palabra in lista_palabras:
										
										for idx, item in enumerate(lista_words):
												
											if item['palabra'] == palabra:
												contador = item['contador'] + 1
												replace_object['palabra'] = palabra
												replace_object['contador'] = contador
												lista_words[idx] = replace_object
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
											#Lista de Palabras por review
											lista_palabras.append(palabra)
											#Guarda palabras nuevas con el contador igual a 1
											element_object['palabra'] = palabra
											element_object['contador'] = 1
											
											lista_words.append(element_object)
											element_object = {}
							
							for word in lista_words:
								lista_object['location'] = location
								palabra = word['palabra'].lower()
								tam_palabra = len(palabra) /2
								mitad_palabra = palabra[:tam_palabra]

								for word_dict in list_dict_positivo:
									if mitad_palabra in word_dict:
										lista_object['frequency_word'] = word
										lista_positiva.append(lista_object)
										lista_object = {}
										break
								lista_object['location'] = location
								for word_dict in list_dict_negativo:
									if mitad_palabra in word_dict:
										lista_object['frequency_word'] = word
										lista_negativa.append(lista_object)
										lista_object = {}
										break
								lista_object['location'] = location
								for word_dict in list_dict_neutral:
									if mitad_palabra in word_dict:
										lista_object['frequency_word'] = word
										lista_neutral.append(lista_object)
										lista_object = {}
										break
							

				data_loactiom_frequency_positivo.write(unicode(js.dumps(lista_positiva, ensure_ascii=False)))
				data_loactiom_frequency_negativo.write(unicode(js.dumps(lista_negativa, ensure_ascii=False)))
				data_loactiom_frequency_neutral.write(unicode(js.dumps(lista_neutral, ensure_ascii=False)))
	data_loactiom_frequency_positivo.close()
	data_loactiom_frequency_negativo.close()
	data_loactiom_frequency_neutral.close()
	

if __name__ == '__main__':
	#frecuencia_data_hotels()
	frecuencia_data_location('FileTokenizationHotelsGeolocalizedSpanish.text', 'location_word_frequency_hotels_spanish_positive.text', 'location_word_frequency_hotels_spanish_negative.text','location_word_frequency_hotels_spanish_neutral.text', 'location_hotel')
	frecuencia_data_location('FileTokenizationActivitiesGeolocalizedSpanish.text', 'location_word_frequency_activities_spanish_positive.text', 'location_word_frequency_activities_spanish_negative.text','location_word_frequency_activities_spanish_neutral.text', 'location_actividad')
	#frecuencia_data('FileTokenizationHotelsGeolocalizedEnglish.text', 'frecuencia_data_set_hotels_English.csv')
	#frecuencia_data('FileTokenizationActivitiesGeolocalizedSpanish.text', 'frecuencia_data_set_activities_Spanish.csv')
	#frecuencia_data('FileTokenizationActivitiesGeolocalizedEnglish.text', 'frecuencia_data_set_activities_English.csv')



