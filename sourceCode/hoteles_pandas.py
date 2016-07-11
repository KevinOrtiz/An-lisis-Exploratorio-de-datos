# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import pandas as pd
import numpy as np
from pandas import Series
import csv

def add_category_hotels():
	hotels = pd.read_csv("../data/TripAdvisor/pdata_final_hotel_co.csv")

	#Convierto los datos de los rating a FLOAT
	hotels['RATING'] = hotels['RATING'].astype(float)
	hotels['CATEGORY'] = hotels['RATING'].map(lambda x: 'Excelente' if (x >= 4 and x <= 5) 
														else 'Bueno' if (x >= 2.5 and x < 4) 
														else 'Regular')
	#hotels = hotels[hotels['longitude']!='None']
	#Guardo el dataframe de actividades en un nuevo archivo CSV
	hotels.to_csv('../data/TripAdvisor/pdata_hotel_categorizado_co.csv', index=False)

if __name__ == '__main__':
	add_category_hotels()