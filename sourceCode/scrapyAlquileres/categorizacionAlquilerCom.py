import pandas as pd
import csv

def rankingreviews():
	datos =pd.read_csv('Alquiler_es.csv',index_col=0)
	datos['top'] = datos['votes_helpful'].map(lambda x: 1 if (x>200)
													else 2 if (x>=100 and x<=200)
													else 3 if (x>50 and x<100)
													else 4 if (x>30 and x<50)
													else 5 )
	datos['local/extranjero'] = datos['location_review'].apply(categorizarextranjero)
	datos.to_csv('Alquiler_es_top.csv')
	


def categorizarextranjero(x):
	if "Ecuador" in x :
		return 'L'
	elif x == '0':
		return 'N'
	else :
		return 'E'


if __name__ == '__main__':
	rankingreviews() 
	