# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import pandas as pd
import numpy as np
from pandas import Series

def add_category_hoteles(name_file):
	hoteles = pd.read_csv(name_file)

	#Convierto los datos de los rating a FLOAT
	hoteles['Rating_Hotel'] = hoteles['Rating_Hotel'].astype(float)
	hoteles['Category_Hotel'] = hoteles['Rating_Hotel'].map(lambda x: 'Excelente' if (x >= 4 and x <= 5) 
														else 'Bueno' if (x >= 2.5 and x < 4) 
														else 'Regular')
	
	#Ordenar el dataframe a partir de la longitud y latitud
	hotels_sort_location = hoteles.sort(['Longitude', 'Latitude'], ascending=[1, 1])
	#crear una columna al dataframe Origen_Username
	hotels_sort_location['Origen_Username'] = hotels_sort_location['City_Username'].map(
												lambda x: 'L' if (x == "Quito") else 'E' )

	#Guardo el dataframe de hoteles en un nuevo archivo CSV
	hotels_sort_location.to_csv('../data_set_hoteles_categorizado.csv', index=False)

def add_category_actividades(name_file):
	actividades = pd.read_csv(name_file)

	#Convierto los datos de los rating a FLOAT
	actividades['Rating_Actividades'] = actividades['Rating_Actividades'].astype(float)
	actividades['Category_Actividades'] = actividades['Rating_Actividades'].map(lambda x: 'Excelente' if (x >= 4 and x <= 5) 
														else 'Bueno' if (x >= 2.5 and x < 4) 
														else 'Regular')
	#Ordenar el dataframe a partir de la longitud y latitud
	actividades_sort_location = actividades.sort(['Longitude', 'Latitude'], ascending=[1, 1])
	#crear una columna al dataframe Origen_Username
	actividades_sort_location['Origen_Username'] = actividades_sort_location['City_Username'].map(
												lambda x: 'L' if (x == "Quito") else 'E' )

	#Guardo el dataframe de hoteles en un nuevo archivo CSV
	actividades_sort_location.to_csv('../data_set_actividades_categorizado.csv', index=False)


if __name__ == '__main__':
	add_category_hoteles("../data_set_hoteles.csv")
	add_category_actividades("../data_set_actividades.csv")