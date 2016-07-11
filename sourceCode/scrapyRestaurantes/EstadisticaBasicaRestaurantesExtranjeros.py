import pandas as pd
import csv

def estadisticabasica():
	datos = pd.read_csv('restaurantes_col.csv',index_col=0)
	##LAS ESTADISTICA LAS OBTENGO POR EL RATING
	datasetEstadisticabasica = pd.DataFrame()
	datasetEstadisticabasica = datos['rating'].describe()

	datasetEstadisticabasica.to_csv('estadisticabasicaRestaurantesLocales.csv')


if __name__ == '__main__':
	estadisticabasica()