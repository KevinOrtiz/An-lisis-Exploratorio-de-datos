import json
import json as js
import io
import re
import os
import string

def get_name_comments_location_hotels_activities_restaurants(input_file_hotels, input_file_activities, input_file_restaurants, dominio):

	with open(input_file_hotels) as data_file1:
		data_json_hotels = json.load(data_file1)

	with open(input_file_activities) as data_file2:
		data_json_activities = json.load(data_file2)

	with open(input_file_restaurants) as data_file3:
		data_json_restaurants = json.load(data_file3)

	csv_file = create_file('Location_Comments', dominio,'coordenadas_lugares')
	cabecera_csv = 'Name_poi,Lat,Lon,NoComments\n'			#Creo la cabecera del CSV
	csv_file.write(cabecera_csv)


	for element in data_json_hotels:
		location = element['location_hotel']
		if location[0] is not None and location[1] is not None:

			lng = location[0]
			lat= location[1]
			name_place = element['name_hotel']

			reviews = element['reviews_hotel']
			if reviews:
				no_reviews = len(reviews)
				csv_file.write(str(name_place)+','+str(lat)+','+str(lng)+','+str(no_reviews)+'\n')

	for element in data_json_activities:
		location = element['location_actividad']
		if location[0] is not None and location[1] is not None:

			lng = location[0]
			lat= location[1]

			name_place = element['name_actividad']

			reviews = element['reviews_actividad']
			if reviews:
				no_reviews = len(reviews)
				csv_file.write(str(name_place)+','+str(lat)+','+str(lng)+','+str(no_reviews)+'\n')

	for element in data_json_restaurants:
		location = element['posicion']
		if location[0] is not None and location[1] is not None:

			lat= location[1]
			lng = location[0]

			name_place = element['tituloLugar']

			reviews = element['itemsReviews']
			if reviews:
				no_reviews = len(reviews)
				csv_file.write(str(name_place)+','+str(lat)+','+str(lng)+','+str(no_reviews)+'\n')

	csv_file.close()


def create_file(folder,dominio, filename):
	name_hotel = str(folder+'/'+dominio+'/'+filename+'_'+dominio+'.csv')
	return  open(''+name_hotel,'w')


if __name__ == '__main__':

	get_name_comments_location_hotels_activities_restaurants("../dataset/data_set_hotels_location_co.json", "../dataset/data_set_activities_location_co.json", "../dataset/data_set_restaurants_location_co.json",'co')
	get_name_comments_location_hotels_activities_restaurants("../dataset/data_set_hotels_location_com.json", "../dataset/data_set_activities_location_com.json", "../dataset/data_set_restaurants_location_com.json",'com')

	print "FIN"