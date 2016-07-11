# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import pandas as pd
import numpy as np
from pandas import Series

def add_category_actividades(name_file):
	actividades = pd.read_csv(name_file)

	#Convierto los datos de los rating a FLOAT
	actividades['RATING'] = actividades['RATING'].astype(float)
	actividades['CATEGORY'] = actividades['RATING'].map(lambda x: 'Excelente' if (x >= 4 and x <= 5) 
														else 'Bueno' if (x >= 2.5 and x < 4) 
														else 'Regular')
	#hotels = hotels[hotels['longitude']!='None']
	#Guardo el dataframe de actividades en un nuevo archivo CSV
	actividades.to_csv('../data/TripAdvisor/pdata_actividades_categorizado_co.csv', index=False)

if __name__ == '__main__':
	add_category_actividades("../data/TripAdvisor/pdata_final_actividades_co.csv")