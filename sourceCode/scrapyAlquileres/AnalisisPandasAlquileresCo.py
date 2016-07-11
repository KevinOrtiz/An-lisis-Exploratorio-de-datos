import pandas as pd
import csv

def procesamientoAlquilerCo():
	datos = pd.read_csv('Alquiler_es.csv',index_col=0)
	datos['precio'] = datos['precio'].astype(float) 
	datos['categorias'] = datos['precio'].map(lambda x: 'Expensive' if (x>300)
										else 'Normal' if (x<300 and x>200)
										else 'economics' if(x<200 and x>100)
										else 'unexpensive')

	datos.to_csv("alquileres_categorias_es.csv")


if __name__ == '__main__':
	procesamientoAlquilerCo()


