import json
import csv
import string
def getDataJson():
	with open('salidaAlquileres.json') as dataFile:
		dataJson = json.load(dataFile)

	csvAlquileres = open('Alquileres.csv','w')
	headAlquileres = 'name,longitude,latitude,precio'
	csvAlquileres.write(headAlquileres)

	for element in dataJson:
		location = element['posicion']
		lng = location[0]
		lat = location[1]
		if not (lng is None and lat is None):
			name = element['tituloLugar']
			name = string.replace(name,',','')
			precio = element['precio']
			line = str(name) + ',' + str(lng) + ',' + str(lat) + ',' + str(precio)+'\n'
			csvAlquileres.write(line)

if __name__ == '__main__':
	getDataJson()
