import string
import unidecode
import json as js
import json
import io

def get_place_location(input_file, output_file, dominio):
	with open(input_file) as data_file:
		data_json = json.load(data_file)

	lista = []
	with io.open(output_file,'w',encoding='utf-8') as file_json:

		for element in data_json:
			location = element['posicion']
			lng = location[0]
			lat = location[1]
			if not (lng is None and lat is None):
				lista.append(element)
		file_json.write(unicode(js.dumps(lista, indent=4, ensure_ascii=False, sort_keys=True, separators=(',',':'))))
	file_json.close()


if __name__ == '__main__':

	print "RESTAURANTES CO"
	get_place_location('../dataset/restaurantes_co.json', '../dataset/data_set_restaurants_location_co.json','co')
	print "RESTAURANTES COM"
	get_place_location('../dataset/restaurantes_com.json', '../dataset/data_set_restaurants_location_com.json', 'com')