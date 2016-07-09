dimport pandas as pd

##Analisis de los datos de los restaurantes

def categoriaRestaurantes():
	data = pd.read_csv('restaurantes.csv',index_col=0)

#print data['tags']

#print data['latitude']

#print data['longitude']

####categorizar por estrellas
	data['rating'] = data['rating'].astype(float) 

	data['categorias'] = data['rating'].map(lambda x:'Excelente' if (x==5)
										else 'Muy Bueno' if (x<5 and x>=4)
										else 'Bueno' if (x<4 and x>=3)
										else 'Regular' if(x>=2 and x<3)
										else 'Indeseable')
	data.to_csv('restaurantes_categorias.csv')


if __name__ == '__main__':
	categoriaRestaurantes()
