# -*- coding: utf-8 -*-

__author__ = 'josanvel'

import pandas as pd
import numpy as np
from pandas import Series

def add_category_actividades():
	actiidades = pd.read_csv("../data/TripAdvisor/nuevo_data_actividades.csv")

	#Convierto los datos de los rating a FLOAT
	actiidades['rating'] = actiidades['rating'].astype(float)
	actiidades['category'] = actiidades['rating'].map(lambda x: 'Excelente' if (x > 4 and x <= 5) 
														else 'Bueno' if (x > 2 and x <= 4) 
														else 'Regular')
	#Guardo el dataframe de actividades en un nuevo archivo CSV
	actiidades.to_csv('../data/TripAdvisor/data_actividades_categorizado.csv')

if __name__ == '__main__':
	add_category_actividades()