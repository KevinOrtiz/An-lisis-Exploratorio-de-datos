import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_graphics_hotels(name_file):

	#Abrir el archivo .CSV
	df_hotel = pd.read_csv(name_file)
	#Ordenar el dataframe a partir de la longitud y latitud
	hotels_sort_location = df_hotel.sort(['LONGITUDE', 'LATITUDE'], ascending=[1, 1])

	#creo dataframe con nueva nacionalidad
	hotels_sort_location['NATIONALITY'] = hotels_sort_location['COUNTRY'].map(
												lambda x: 'L' if (x == "Ecuador") else 'E' )
	
	#Creo un diagrama de barra a partir de una estadistica descriptivs
	nacionality_rating = hotels_sort_location[["NATIONALITY","RATING"]].groupby("NATIONALITY").agg([('Min','min'), ('Media','mean'),('Max','max')])
	#fig = plt.figure()
	#fig.suptitle('Diagrama de Barrar -- Rating vs NAtionality')
	
	plt_nacionality_rating = nacionality_rating.plot(kind='bar')
	plt_nacionality_rating.set_ylabel("RATING")
	plt.title('Diagrama de Barras')
	plt.legend(('Rating','Min','Media','Max'), loc='best')

	#Proyeccion de nacionalida,rating y helpful
	nat_rat_help = hotels_sort_location[["NATIONALITY","RATING","HELPFUL"]]

	#Diagrama de puntos a partir de los votos utilies entre locales y extranjeros
	df_local = hotels_sort_location[hotels_sort_location["NATIONALITY"] == "L"]
	df_extranjero = hotels_sort_location[hotels_sort_location["NATIONALITY"] == "E"]

	df_local.plot(kind='scatter', x='HELPFUL', y='RATING', color='DarkBlue', label='Local')
	df_extranjero.plot(kind='scatter', x='HELPFUL', y='RATING',color='DarkGreen', label='Extranjero');

	#Mostrar todos los diagramas
	#plt.show()

	#Numero de Usuario 
	count_user_hotels = hotels_sort_location.USER.nunique()
	print "Numero-Usuario CosasQueHacer-TripAvisor",count_user_hotels 

	#Dataframe agrupado por Hoteles y ccuenta cuantos usuarios locales y extranjero tuvo
	#Cuento por usuarios locales y extranjeros
	local = lambda x: x[ hotels_sort_location['NATIONALITY'] == 'E'].count()
	extranjero = lambda y: y[hotels_sort_location['NATIONALITY'] == 'L'].count()
	#Funcion para agregar el numero de usuarios locales y extranjeros
	funcion_nationality = [('local', local), ('extranjero', extranjero)]
	group_hotels_nationality = hotels_sort_location[["NAME","NATIONALITY"]].groupby('NAME').agg(funcion_nationality)

	data = group_hotels_nationality.add_suffix('_Count').reset_index()
	#print data
	print data.ix[data[('NATIONALITY_Count', 'local_Count')].idxmax()]
	#print list(data)


if __name__ == '__main__':
	get_graphics_hotels("../data/TripAdvisor/pdata_actividades_categorizado_com.csv")