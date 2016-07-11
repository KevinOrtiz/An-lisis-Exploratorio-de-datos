import pandas as pd
import csv

def rankingreviews():
	datos =pd.read_csv('restaurantes_col.csv',index_col=0)
	datos['top'] = datos['Nvotos_utiles'].map(lambda x: 1 if (x>=500)
													else 2 if (x>=300 and x<=400)
													else 3 if (x>200 and x<300)
													else 4 if (x>100 and x<200)
													else 5 )
	datos['local/extranjero'] = datos['Pais'].apply(categorizarextranjero)
	datos.to_csv('restaurantes_col_top.csv')
	


def categorizarextranjero(x):
	if x == " Ecuador" :
		return 'L'
	elif x == '0':
		return 'N'
	else :
		return 'E'


if __name__ == '__main__':
	rankingreviews() 