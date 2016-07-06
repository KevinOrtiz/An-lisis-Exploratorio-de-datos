import json
import csv
import string
def getDataJson():
	with open('salida.json') as dataFile:
		dataJson = json.load(dataFile)

	csvRestaurantes = open('restaurantes.csv','w')
	headRestaurantes = 'name,longitude,latitude,rating,NoReviews,tags'
	csvRestaurantes.write(headRestaurantes)

	for element in dataJson:
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
			for tag in tags:
				line_tags = line_tags + '$' + tag

			line = str(name) + ',' + str(lng) + ',' + str(lat) + ',' + str(rating) + ',' + str(NoReviews)+ ',' + str(line_tags)+'\n'
			if rating:
				csvRestaurantes.write(line)

if __name__ == '__main__':
	getDataJson()
