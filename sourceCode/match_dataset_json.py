# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import json
import csv
import string
import unidecode

"""
Funcion: 		match_get_data_hotel
Autor: 			Jose Velez Gomez
Descripcion: 	Une las dos dataset con dominios .COM --- .CO , para obtener los datos 
				y guardarlos en un .CSV
Estado: 		Terminado
"""
def match_get_data_hotel():
	#Abro el archivo JSON de los hoteles
	with open('scrapy_hotel/scrapy_hotel/spiders/data_set_hotel_co.json') as data_file1:
		data_json1 = json.load(data_file1)

	with open('scrapy_hotel/scrapy_hotel/spiders/data_set_hotel_com.json') as data_file2:
		data_json2 = json.load(data_file2)

	#Creo el archivo CSV
	csv_file = open('../data_set_hoteles.csv', 'w')
	#Creo la cabecera del CSV
	cabecera_json = 'Name_Hotel,Rating_Hotel,NumOpinionesHotel,Longitude,Latitude,Username,DateReview,HelpfulReview,OpinionsUserReview,City_Username,Country_Username\n'
	#Guardo la cabecera en el archivo CSV
	csv_file.write(cabecera_json)

	for element1 in data_json1:
		for x, element2 in enumerate(data_json2):
			if element1["name_hotel"] == element2["name_hotel"]:
				
				location = element1['location_hotel']
				lng = location[0]
				lat = location[1]

				if not (lng is None and lat is None):

					#===========Verifica que el registro tengo RATING
					rating = element1['rating_hotel']					#Obtengo el raiting de la Actividad
					
					if rating:
						rating = string.replace(rating, ',', '.')
						name = element1['name_hotel']					#Obtengo el nombre de un hotel
						name = string.replace(name, ',', '')	

						num_opiniones_hotel = element1['opinions_hotel']

						reviews1 = element1['reviews_hotel']
						reviews2 = element2['reviews_hotel']
						reviews = reviews1 + reviews2					#Obtengo los reviews de un hotel
						#print reviews			
						NoReviews = len(reviews)						#Obtengo el numoero de reviews de un hotel

						if NoReviews > 0:
							for review in reviews:
								if review:
									user = review['username_review']
									if user:
										#user = string.replace(user, ',', '')
										date_review = review['date_review']

										if date_review:
											date_review = string.replace(date_review, 'Escribio una opinion el ', '')
											date_review = string.replace(date_review, 'Reviewed ', '')
											date_review = string.replace(date_review, ',', '')
											date_review = date_review.split(' ')
											date_review = change_date(date_review)

										if user:
											user = string.replace(user, ',', '')
										else:
											user = None

										location_user = review['location_review']
										if location_user:
											location_user = unidecode.unidecode(location_user)
											location_user = location_user.split(', ')

											if location_user[0].isdigit():
												location_user.remove(location_user[0])

											if len(location_user) > 2:
												country = location_user[2]
												city = location_user[0]+' '+location_user[1]
											elif len(location_user) == 2:
												city = location_user[0]
												country = location_user[1]
											elif len(location_user) == 1:
												city = location_user[0]
												country = city
											else:
												city = None
												country = city
					
										else:
											city = None
											country = city

										helpful = review['helpful_review']
										if not helpful:
											helpful = 0

										opinions = review['opinions_user_review']
										if not opinions:
											opinions = 0
											
										#Concateno la linea del CSV
										line = str(name)+','+str(rating)+','+str(num_opiniones_hotel)+','+str(lng)+','+str(lat)+','+str(user)+','+str(date_review)+','+str(helpful)+','+str(opinions)+','+str(city)+','+str(country)+'\n'									
										#Guardo la linea en el archivo CSV
										csv_file.write(line)


"""
Funcion: 		match_get_data_actividades
Autor: 			Jose Velez Gomez
Descripcion: 	Une las dos dataset con dominios .COM --- .CO , para obtener los datos 
				y guardarlos en un .CSV
Estado: 		Terminado
"""
def match_get_data_actividades():
	#Abro el archivo JSON de los hoteles
	with open('scrapy_hotel/scrapy_hotel/spiders/data_set_actividades_co.json') as data_file1:
		data_json1 = json.load(data_file1)

	with open('scrapy_hotel/scrapy_hotel/spiders/data_set_actividades_com.json') as data_file2:
		data_json2 = json.load(data_file2)

	#Creo el archivo CSV
	csv_file = open('../data_set_actividades.csv', 'w')
	#Creo la cabecera del CSV
	cabecera_json = 'Name_Actividades,Rating_Actividades,NumOpiniones_Actividades,Longitude,Latitude,Username,DateReview,HelpfulReview,OpinionsUserReview,City_Username,Country_Username,TagsActividad\n'
	#Guardo la cabecera en el archivo CSV
	csv_file.write(cabecera_json)

	for element1 in data_json1:
		for x, element2 in enumerate(data_json2):
			if element1["name_actividad"] == element2["name_actividad"]:
				
				location = element1['location_actividad']
				lng = location[0]
				lat = location[1]

				if not (lng is None and lat is None):
					#===========Verifica que el registro tengo RATING
					rating = element1['rating_actividad']					#Obtengo el raiting de la Actividad

					if rating:
						rating = string.replace(rating, ',', '.')
						name = element1['name_actividad']					#Obtengo el nombre de la Actividad
						name = string.replace(name, ',', '')	

						num_opiniones_hotel = element1['opinions_actividad']

						reviews1 = element1['reviews_actividad']
						reviews2 = element2['reviews_actividad']
						reviews = reviews1 + reviews2					#Obtengo los reviews de la Actividad
						#print reviews			
						NoReviews = len(reviews)						#Obtengo el numoero de reviews de la Actividad
						tags_actividades = element1['tags_categorias_actividades']

						if NoReviews > 0:
							for review in reviews:
								line_tags = ""
								for tag in tags_actividades:
									line_tags = line_tags+'$'+tag

								if review:
									user = review['username_review']
									if user:
										date_review = review['date_review']

										if date_review:
											date_review = string.replace(date_review, 'Escribio una opinion el ', '')
											date_review = string.replace(date_review, 'Reviewed ', '')
											date_review = string.replace(date_review, ',', '')
											date_review = date_review.split(' ')
											date_review = change_date(date_review)

										if user:
											user = string.replace(user, ',', '')
										else:
											user = None
										
										location_user = review['location_review']
										if location_user:
											location_user = unidecode.unidecode(location_user)
											location_user = location_user.split(', ')

											if location_user[0].isdigit():
												location_user.remove(location_user[0])

											if len(location_user) >= 3:
												country = location_user[2]
												city = location_user[0]+' '+location_user[1]
											elif len(location_user) == 2:
												city = location_user[0]
												country = location_user[1]
											elif len(location_user) == 1:
												city = location_user[0]
												country = city
											else:
												city = None
												country = city
						
										else:
											city = None
											country = city

										helpful = review['helpful_review']
										if not helpful:
											helpful = 0
										
										opinions = review['opinions_user_review']
										if not opinions:
											opinions = 0

										#Concateno la linea del CSV
										line = str(name)+','+str(rating)+','+str(num_opiniones_hotel)+','+str(lng)+','+str(lat)+','+str(user)+','+str(date_review)+','+str(helpful)+','+str(opinions)+','+str(city)+','+str(country)+','+str(line_tags)+'\n'
										#Guardo la linea en el archivo CSV
										csv_file.write(line)


"""
Funcion: 		change_date
Autor: 			Jose Velez Gomez
Descripcion: 	Crear a partir de un string la fecha con formato dd/mm/aaaa
Estado: 		Terminado
"""
def change_date(list_date):
	
	if list_date[0].isdigit():
		dia = list_date[0]
		mes = change_month(list_date[1])
		anio = list_date[2]
	else:
		dia = list_date[1]
		mes = change_month(list_date[0])
		anio = list_date[2]
	fecha = dia+'/'+mes+'/'+anio

	return fecha


"""
Funcion: 		change_month
Autor: 			Jose Velez Gomez
Descripcion: 	Obtiene el numero del mes correspondiente al string en ingles o espanol
Estado: 		Terminado
"""
def change_month(month):
	if month=="enero" or month=="January":
		mes = '01'
	elif month=="febrero" or month=="February":
		mes = '02'
	elif month=="marzo" or month=="March":
		mes = '03'
	elif month=="abril" or month=="April":
		mes = '04'
	elif month=="mayo" or month=="May":
		mes = '05'
	elif month=="junio" or month=="June":
		mes = '06'
	elif month=="julio" or month=="July":
		mes = '07'
	elif month=="agosto" or month=="August":
		mes = '08'
	elif month=="septiembre" or month=="September":
		mes = '09'
	elif month=="octubre" or month=="October":
		mes = '10'
	elif month=="noviembre" or month=="November":
		mes = '11'
	elif month=="diciembre" or month=="December":
		mes = '12'
	return mes


if __name__ == '__main__':
	match_get_data_hotel()
	match_get_data_actividades()