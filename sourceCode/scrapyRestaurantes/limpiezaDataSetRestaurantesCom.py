import json
import csv
import string

def getDataJson():
	with open('salidaRestaurantePrueba.json') as file:
		data =json.load(file)

	csvRestaurantes = open('restaurantes_col.csv','w')
	head_restaurantes = 'name,longitude,latitude,rating,NoReviews,tags,ciudad_usuario,Pais,Nvotos_restaurantes,Nvotos_utiles,fecha_opinion,year,\n'
	csvRestaurantes.write(head_restaurantes)
	Nvotos_restaurantes = 0
	Nvotos_utiles = 0
	
	for element in data:
		location = element['posicion']
		lng = location[0]
		lat = location[1]
		if not (lng is None and lat is None):
			name = element['tituloLugar']
			name = string.replace(name,',','')
			rating = element['estrellas']
			reviews = element['itemsReviews']
			NoReviews = len(reviews)
			tags = element['tags']
			line_tags = ""
			for y,x in enumerate(reviews):
				if not(x['numero_restaurant_review'] == '' or x['votos_utiles'] == '' or x['origen_usuario'] == '' or x['date_review'] == ''):
					Nvotos_restaurantes = x['numero_restaurant_review']
					Nvotos_utiles = x['votos_utiles']
					ciudad_usuario = x['origen_usuario'] 
					fecha_review = x['date_review']
					for tag in tags:
						line_tags = line_tags + '$' + tag
					for j,k,l,m in map(None,fecha_review,ciudad_usuario,Nvotos_utiles,Nvotos_restaurantes):
						
						print j,k,l,m

						line = str(name) + ',' + str(lng) + ',' + str(lat) + ',' + str(rating) + ',' + str(NoReviews) + ',' + str(line_tags) + ',' + str(k) + ',' + str(m) + ',' + str(l) + ',' + str(j)+'\n'
			if 1:
				csvRestaurantes.write(line)
if __name__ == '__main__':
	getDataJson()




