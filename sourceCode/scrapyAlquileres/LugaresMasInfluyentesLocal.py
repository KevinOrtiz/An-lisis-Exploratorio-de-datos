import pandas as pd
import csv

def rankingreviews():
	datos =pd.read_csv('Alquiler_col.csv',index_col=0)
	datos['opinions_review'] = datos['opinions_review'].astype(int) 
	datos['Lugares_mayor_review'] = datos['opinions_review'].map(lambda x: 1 if (x>=100)
													else 2 if (x<100 and x>=70)
													else 3 if (x>=30 and x<70)
													else 4 if (x>=10 and x<30)
													else 5 )
	datos['local/extranjero'] = datos['location_review'].apply(categorizarextranjero)
	datos.to_csv('Alquiler_col_influyente.csv')
	


def categorizarextranjero(x):
	if "Ecuador" in x :
		return 'L'
	elif x == '0':
		return 'N'
	else :
		return 'E'


if __name__ == '__main__':
	rankingreviews() 
	