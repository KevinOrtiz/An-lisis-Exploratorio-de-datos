import json as js
import io
import re
import os
import string


"""
Funcion:        create_user_location_hotels
Autor:          Jose Velez Gomez
Descripcion:    Crea una archivo CSV de los usuarios con el lugar deu hizo el review.
Estado:         Terminado
"""
def create_user_location_hotels(input_file, output_file, dominio):

	list_hotels = []
	list_user_hotels = {}

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	
	with io.open('Hoteles/User_Location/'+dominio+'/user_location_'+dominio+'.json','w',encoding='utf-8') as json_file:
		for element in data_json:
			location = element['location_hotel']
			if location[0] is not None and location[1] is not None:
				place = element['name_hotel']

				if element['reviews_hotel']:
					for review in element['reviews_hotel']:
						if review:
							user = review['username_review']
							if user:
								helpful = review['helpful_review']
								list_user_hotels['username_review'] = user
								list_user_hotels['location_hotel'] = location
								list_user_hotels['name_hotel'] = place
								list_user_hotels['helpful_review'] = helpful
								
					list_hotels.append(list_user_hotels)
					list_user_hotels = {}
		json_file.write(unicode(js.dumps(list_hotels, ensure_ascii=False)))
	json_file.close()


"""
Funcion:        create_user_location_activities
Autor:          Jose Velez Gomez
Descripcion:    Crea una archivo CSV de los usuarios con el lugar deu hizo el review.
Estado:         Terminado
"""
def create_user_location_activities(input_file, output_file, dominio):

	list_activities = []
	list_user_activities = {}

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)		

	with io.open('Actividades/User_Location/'+dominio+'/user_location_'+dominio+'.json','w',encoding='utf-8') as json_file:
		for element in data_json:
			location = element['location_actividad']
			if location[0] is not None and location[1] is not None:
				place = element['name_actividad']
				if element['reviews_actividad']:
					for review in element['reviews_actividad']:
						if review:
							user = review['username_review']
							if user:
								helpful = review['helpful_review']
								list_user_activities['username_review'] = user
								list_user_activities['location_actividad'] = location
								list_user_activities['name_actividad'] = place
								list_user_activities['helpful_review'] = helpful

					list_activities.append(list_user_activities)
					list_user_activities = {}
		json_file.write(unicode(js.dumps(list_activities, ensure_ascii=False)))
		json_file.write(unicode('\n'))
	json_file.close()


def create_file(folder,dominio, folder_extension):

	name_hotel = str(folder+'/'+dominio+'/'+'user_location_'+dominio+'.'+folder_extension)
	return  open(''+name_hotel,'w')


if __name__ == '__main__':
	print "USER HOTELES CO"
	create_user_location_hotels("../dataset/data_set_hotels_location_co.json", 'hotels_co', 'co')
	print "USER HOTELES COM"
	create_user_location_hotels("../dataset/data_set_hotels_location_com.json", 'hotels_com', 'com' )
	print "USER ACTIVIDADES CO"
	create_user_location_activities("../dataset/data_set_activities_location_co.json",'activities_co', 'co')
	print "USER ACTIVIDADES COM"
	create_user_location_activities("../dataset/data_set_activities_location_com.json",'activities_com', 'com')