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

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	#Creacion del archivo CSV
	csv_file = create_file('Hoteles/User_Location', dominio, 'csv')
	cabecera_csv = 'User,Location,Place\n'			#Creo la cabecera del CSV
	csv_file.write(cabecera_csv)

	for element in data_json:
		location = element['location_hotel']
		if location[0] is not None and location[1] is not None:
			place = element['name_hotel']

			if element['reviews_hotel']:
				for review in element['reviews_hotel']:
					if review:
						user = review['username_review']
						if user:
							line = str(user)+','+str(location)+','+str(place)+'\n'
							csv_file.write(line)
	csv_file.close()


"""
Funcion:        create_user_location_activities
Autor:          Jose Velez Gomez
Descripcion:    Crea una archivo CSV de los usuarios con el lugar deu hizo el review.
Estado:         Terminado
"""
def create_user_location_activities(input_file, output_file, dominio):

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)
	
	#Creacion del archivo text
	csv_file = create_file('Actividades/User_Location', dominio, 'csv')
	cabecera_csv = 'User,Location,Place\n'			#Creo la cabecera del CSV
	csv_file.write(cabecera_csv)			

	for element in data_json:
		location = element['location_actividad']
		if location[0] is not None and location[1] is not None:
			place = element['name_actividad']
			if element['reviews_actividad']:
				for review in element['reviews_actividad']:
					if review:
						user = review['username_review']
						if user:
							line = str(user)+','+str(location)+','+str(place)+'\n'
							csv_file.write(line)
	csv_file.close()


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