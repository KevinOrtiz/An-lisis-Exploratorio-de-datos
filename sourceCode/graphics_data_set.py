import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_graphics_hotels(name_file):

	#Abrir el archivo .CSV
	df_hotel = pd.read_csv(name_file)
	df_actividades = pd.read_csv("../data_set_actividades_categorizado.csv")
	#print df_hotel.head(5)
	count_user_hotels = df_hotel.Username.nunique()
	#print "\nNumero-Usuario Hotel-TripAvisor",count_user_hotels 
	
	local = lambda x: x[ df_hotel['Origen_Username'] == 'E'].count()
	extranjero = lambda y: y[df_hotel['Origen_Username'] == 'L'].count()
	#Funcion para agregar el numero de usuarios locales y extranjeros
	funcion_Origen= [('Numero_Usuario','count'),('Local', local), ('NoLocal', extranjero)]
	group_hotels_Origen = df_hotel[["Name_Actividades","Origen_Username"]].groupby('Name_Actividades').agg(funcion_Origen)
	
	data = group_hotels_Origen.add_suffix('').reset_index()
	#data.to_csv('../group_actividades_Origen.csv', index=False)


	df_hotel_Origen_actividades = pd.read_csv("../group_actividades_Origen.csv", index_col=0)
	df_hotel_Origen_hoteles = pd.read_csv("../group_hoteles_Origen.csv", index_col=0)

	df_Origen_NoLocal = df_hotel_Origen_actividades.sort(['NoLocal'], ascending=0)
	df_Origen_Local = df_hotel_Origen_actividades.sort(['Local'], ascending=0)
	df_Origen_Local_NoLocal = df_hotel_Origen_actividades.sort(['Numero_Usuario'], ascending=0)

	df_Origen_NoLocal = df_Origen_NoLocal.add_suffix('').reset_index()
	df_Origen_Local = df_Origen_Local.add_suffix('').reset_index()
	df_Origen_Local_NoLocal = df_Origen_Local_NoLocal.add_suffix('').reset_index()

	#print df_Origen_Local_NoLocal#.head(50)
	print"\n\nActividades===\n"
	print df_hotel_Origen_actividades.describe()

	print "Max:",df_Origen_Local_NoLocal.max()
	print "\nPromedio:",df_Origen_Local_NoLocal.mean()
	print "\nMin:",df_Origen_Local_NoLocal.min()
	print "\nSum:",df_Origen_Local_NoLocal.sum()
	#print "\n\nACTIVIDADES\n\n",df_Origen_NoLocal.head(10)
	#print "",df_Origen_Local.head(10)
	#print "",df_Origen_Local_NoLocal.head(10)

	#df_Origen_NoLocal.to_csv("../data/hoteles_Origen_no_local.csv", index_col=0)
	#df_Origen_Local.to_csv("../data/hoteles_Origen_local.csv", index_col=0)
	#df_Origen_Local_NoLocal.to_csv("../data/hoteles_Origen_local_nolocal.csv", index_col=0)

	df_Origen_NoLocal = df_hotel_Origen_hoteles.sort(['NoLocal'], ascending=0)
	df_Origen_Local = df_hotel_Origen_hoteles.sort(['Local'], ascending=0)
	df_Origen_Local_NoLocal = df_hotel_Origen_hoteles.sort(['Numero_Usuario'], ascending=0)

	df_Origen_NoLocal = df_Origen_NoLocal.add_suffix('').reset_index()
	df_Origen_Local = df_Origen_Local.add_suffix('').reset_index()
	df_Origen_Local_NoLocal = df_Origen_Local_NoLocal.add_suffix('').reset_index()
	print"\n\nHoteles===\n"
	print df_hotel_Origen_hoteles.describe()

	print "Max:",df_Origen_Local_NoLocal.max()
	print "\nPromedio:",df_Origen_Local_NoLocal.mean()
	print "\nMin:",df_Origen_Local_NoLocal.min()
	print "\nSum:",df_Origen_Local_NoLocal.sum()


	#print "\n\nHoteles\n\n",df_Origen_NoLocal.head(10)
	#print "",df_Origen_Local.head(10)
	#print "",df_Origen_Local_NoLocal.head(10)
	df_Origen_NoLocal.to_csv("../data/hoteles_Origen_no_local.csv", index_col=0)
	df_Origen_Local.to_csv("../data/hoteles_Origen_local.csv", index_col=0)
	df_Origen_Local_NoLocal.to_csv("../data/hoteles_Origen_local_nolocal.csv", index_col=0)

	#df_Origen_NoLocal.to_csv('../df_sort_origen_no_local_hoteles.csv', index=False)
	#df_Origen_Local.to_csv('../df_sort_origen_local_hoteles.csv', index=False)
	#df_Origen_Local_NoLocal.to_csv('../df_sort_origen_local_no_locales_actividades.csv', index=False)

	#=========Obtengo el dataframe  para obtener el Top Ten de los Ususrio con mayor Helpful votes y # de opniones de esta categoria
	df_user_helpful_reviews  = df_hotel[['Origen_Username','Username','HelpfulReview', 'OpinionsUserReview']].groupby(['Username','Origen_Username']).agg([('mean')])
	df_user_helpful_reviews = df_user_helpful_reviews.add_suffix('').reset_index()

	##=========df_user_helpful_reviews.to_csv('../df_usuario_helpful_opiniones_hoteles.csv', index=False)
	df_user_helpful_reviews_actividades = pd.read_csv("../df_usuario_helpful_opiniones_actividades.csv", index_col=0)
	df_user_helpful_reviews_hotel = pd.read_csv("../df_usuario_helpful_opiniones_hoteles.csv", index_col=0)

	df_user_helpful_reviews_actividades = df_user_helpful_reviews_actividades.sort(['HelpfulReview','OpinionsUserReview'], ascending=[0,0])
	df_user_helpful_reviews_hotel = df_user_helpful_reviews_hotel.sort(['HelpfulReview','OpinionsUserReview'], ascending=[0,0])
	
	#print "\n\nActividades \n",df_user_helpful_reviews_actividades.head(10)
	#print "\n\nHoteles\n",df_user_helpful_reviews_hotel.head(10)
	#print "",df_Origen_Local_NoLocal.head(10)

	#======== Diagrama de Barra

	#Creo un diagrama de barra a partir de una estadistica descriptivs
	nacionality_rating = df_hotel[["Origen_Username","Rating_Actividades"]].groupby("Origen_Username").agg([('Min','min'), ('Media','mean'),('Max','max')])

	plt_nacionality_rating = nacionality_rating.plot(kind='bar')
	plt_nacionality_rating.set_ylabel("Rating_Actividades")
	plt.title('Diagrama de Barras')
	plt.legend(('Rating','Min','Media','Max'), loc='best')

	#Proyeccion de nacionalida,rating y helpful
	nat_rat_help = df_hotel[["Origen_Username","Rating_Actividades","HelpfulReview"]]

	#Diagrama de puntos a partir de los votos utilies entre locales y extranjeros
	df_local = df_hotel[df_hotel["Origen_Username"] == "L"]
	df_extranjero = df_hotel[df_hotel["Origen_Username"] == "E"]

	df_local.plot(kind='scatter', x='HelpfulReview', y='Rating_Actividades', color='DarkBlue', label='Local')
	df_extranjero.plot(kind='scatter', x='HelpfulReview', y='Rating_Actividades',color='DarkGreen', label='Foraneos');

	#Mostrar todos los diagramas
	#plt.show()



	#print df_hotel.head(5)
	#print"\n\n"
	#print group_hotels_nationality.head(5)

	# #Creo un diagrama de barra a partir de una estadistica descriptivs
	# nacionality_rating = hotels_sort_location[["NATIONALITY","RATING"]].groupby("NATIONALITY").agg([('Min','min'), ('Media','mean'),('Max','max')])
	# plt_nacionality_rating = nacionality_rating.plot(kind='bar')
	# plt_nacionality_rating.set_ylabel("RATING")
	# plt.title('Diagrama de Barras')
	# plt.legend(('Rating','Min','Media','Max'), loc='best')

	# #Mostrar todos los diagramas
	# plt.show()

	

if __name__ == '__main__':
	get_graphics_hotels("../data_set_actividades_categorizado.csv")
	#get_graphics_actividades("../data_set_categorizado_hactividades.csv")