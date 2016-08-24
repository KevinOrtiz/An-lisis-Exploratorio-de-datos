import json as js
import io
import string


"""
Funcion:        create_corpus_hotels
Autor:          Jose Velez Gomez
Descripcion:    
Estado:         Terminado
"""
def create_corpus_hotels(input_file, output_file):

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	lista_hotels = []
	lista_Reviews = {}
	lista_comentarios = []
	contador = 0
	
	for element in data_json:
		lista_comentarios = []
		if element['location_hotel'][0] is not None and element['location_hotel'][1] is not None:
			contador = contador + 1
			for review in element['reviews_hotel']:
				if review:
					for text in review['description_review']:
						lista_comentarios.append(text)
				
			nombre_hotel = element['name_hotel']
			nombre_hotel = string.replace(nombre_hotel, " ", '_')
			nombre_hotel = string.replace(nombre_hotel, ".", "")
			nombre_hotel = string.replace(nombre_hotel, ",", "")
			nombre_hotel = string.replace(nombre_hotel, ";", "")
			nombre_hotel = string.replace(nombre_hotel, ":", "")
			nombre_hotel = string.replace(nombre_hotel, "(", "")
			nombre_hotel = string.replace(nombre_hotel, ")", "")
			nombre_hotel = string.replace(nombre_hotel, "-", "_")
			lista_Reviews['reviews'] = lista_comentarios
			
			if lista_Reviews:
				with io.open(output_file+'_'+nombre_hotel+".text",'w',encoding='utf-8') as file_tokenization:
					file_tokenization.write(unicode(js.dumps(lista_Reviews, ensure_ascii=False)))
				file_tokenization.close()

				del lista_comentarios
				lista_Reviews = {}

"""
Funcion:        create_corpus_activities
Autor:          Jose Velez Gomez
Descripcion:    
Estado:         Terminado
"""
def create_corpus_activities(input_file, output_file):

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	lista_activities = []
	lista_Reviews = {}
	lista_comentarios = []
	contador = 0

	for element in data_json:
		lista_comentarios = []
		if element['location_actividad'][0] is not None and element['location_actividad'][1] is not None:
			contador = contador + 1
			for review in element['reviews_actividad']:
				if review:
					for text in review['description_review']:
						lista_comentarios.append(text)
				
			nombre_actividad = element['name_actividad']
			nombre_actividad = string.replace(nombre_actividad, " ", '_')
			nombre_actividad = string.replace(nombre_actividad, ".", "")
			nombre_actividad = string.replace(nombre_actividad, ",", "")
			nombre_actividad = string.replace(nombre_actividad, ";", "")
			nombre_actividad = string.replace(nombre_actividad, ":", "")
			nombre_actividad = string.replace(nombre_actividad, "(", "")
			nombre_actividad = string.replace(nombre_actividad, ")", "")
			nombre_actividad = string.replace(nombre_actividad, "-", "_")

			lista_Reviews['reviews'] = lista_comentarios

			if lista_Reviews:
				with io.open(output_file+'_'+nombre_actividad+".text",'w',encoding='utf-8') as file_tokenization:
					file_tokenization.write(unicode(js.dumps(lista_Reviews, ensure_ascii=False)))
				file_tokenization.close()

				del lista_comentarios
				lista_Reviews = {}


if __name__ == '__main__':

	#create_corpus_hotels("../data_set_hotels_location_co.json", 'corpus_hotels_co')
	#create_corpus_hotels("../data_set_hotels_location_com.json", 'corpus_hotels_com' )

	#create_corpus_activities("../data_set_activities_location_co.json",'corpus_activities_co')
	create_corpus_activities("../data_set_activities_location_com.json",'corpus_activities_com')