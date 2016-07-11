import json
import csv
import string

def getDataJson():
	with open('salida_alquiler_com.json') as file:
		data =json.load(file)

	csvAlquiler= open('Alquiler_es.csv','w')
	head_Alquiler = 'name,longitude,latitude,precio,location_review,opinions_review,votes_helpful,user_review,\n'
	csvAlquiler.write(head_Alquiler)
	
	for element in data:
		location = element['location']
		lng = location[0]
		lat = location[1]
		datos = element['reviews']
		if not(lng is None and lat is None):	
			for valor in datos:
				name = element['name']
				name = string.replace(name,',','')
				precio = element['precio']
				locacion_review = valor['location_review']
				numero_opiniones = valor['opinions_review']
				numero_opiniones_utiles = valor['votes_helpful']
				user = valor['user_review']
				line = str(name) + ',' + str(lng) + ',' + str(lat) + ',' + str(precio) + ',' + str(locacion_review ) + ',' + str(numero_opiniones) + ',' + str(numero_opiniones_utiles) + ',' + str(user) + '\n'
				csvAlquiler.write(line)

			

if __name__ == '__main__':
	getDataJson()
