import pandas as pd
import csv

def rankingreviews():
	datos =pd.read_csv('restaurantes_extranjeros.csv',index_col=0)
	datos['Nvotos_restaurantes'] = datos['Nvotos_restaurantes'].astype(int) 
	datos['mayor_influencia'] = datos['Nvotos_restaurantes'].map(lambda x: 1 if (x>100 and x<=200)
													else 2 if (x>=80 and x<100)
													else 3 if (x>50 and x<80)
													else 4 if (x>10 and x<50)
													else 5 )
	datos['local/extranjero'] = datos['Pais/Estado'].apply(categorizarextranjero)
	datos.to_csv('restaurantes_es_influencia.csv')
	


def categorizarextranjero(x):
	if x == " Ecuador" :
		return 'L'
	elif x == '0':
		return 'N'
	else :
		return 'E'


if __name__ == '__main__':
	rankingreviews() 