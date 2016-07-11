import pandas as pd
import csv

def analisisRestaurantes():
	datos = pd.read_csv('restaurantes_extranjeros.csv',index_col=0)

	datos['rating'] = datos['rating'].astype(float) 

	datos['categorias'] = datos['rating'].map(lambda x: 'Excelente' if (x==5)
										else 'muy bueno' if (x<4 and x>3.5)
										else 'Regular' if(x<3 and x>2)
										else 'Pesimo')

	datos.to_csv('Restaurantes_categorias_extranjeros.csv')


if __name__ == '__main__':
	analisisRestaurantes()
