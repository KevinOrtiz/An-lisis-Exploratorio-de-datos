# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import pandas as pd
import numpy as np
from pandas import Series

def add_category_hotels():
	hotels = pd.read_csv("../data/TripAdvisor/nuevo_data_hotel.csv")

	#Convierto los datos de los rating a FLOAT
	hotels['rating'] = hotels['rating'].astype(float)
	hotels['category'] = hotels['rating'].map(lambda x: 'Excelente' if (x > 4 and x <= 5) 
														else 'Bueno' if (x > 2 and x <= 4) 
														else 'Regular')
	#Guardo el dataframe de actividades en un nuevo archivo CSV
	hotels.to_csv('../data/TripAdvisor/data_hotel_categorizado.csv')

if __name__ == '__main__':
	add_category_hotels()