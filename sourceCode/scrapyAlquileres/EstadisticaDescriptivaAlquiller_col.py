import pandas as pd
import csv

def procesamiento():
	datos = pd.read_csv('alquileres_categorias_es.csv',index_col=0)
	Alquileres_Espanol = pd.DataFrame()
	Alquileres_Espanol['#expensive'] = datos[datos['categorias']=='expensive'].count()
	Alquileres_Espanol['#economics'] = datos[datos['categorias']=='economics'].count()
	Alquileres_Espanol['#unexpensive'] = datos[datos['categorias']=='unexpensive'].count()
	Alquileres_Espanol['mediana'] = datos['precio'].mean()
	Alquileres_Espanol['maximo'] = datos['precio'].max()
	Alquileres_Espanol['minimo'] = datos['precio'].min()
	Alquileres_Espanol.to_csv("AlquileresEuropa.csv")

if __name__ == '__main__':
	procesamiento()