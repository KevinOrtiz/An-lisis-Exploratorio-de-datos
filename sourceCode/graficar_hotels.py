import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_graphics_hotels(name_file):
	df_hotel = pd.read_csv(name_file, index_col=0)
	#df_hotel['LONGITUDE'] = df_hotel['LONGITUDE']#.astype(float)
	#df_hotel['NoOpinionsHotels'] = df_hotel['NoOpinionsHotels'].astype(float)


	hotels_sort_location = df_hotel.sort(['LONGITUDE', 'LATITUDE'], ascending=[1, 1])
	#print hotels_sort_location

	hotels_sort_location['NACIONALITY'] = hotels_sort_location['COUNTRY'].map(
												lambda x: 'L' if (x == "Ecuador") 
																else 'E' )
	#print 
	#print hotels_sort_location.groupby('NACIONALITY').NoOpinionsHotels.apply(lambda x: pd.Series({'max':x.max(),'min':x.min(),'mean':x.mean()}))

	#print hotels_sort_location.groupby('NACIONALITY').NoOpinionsHotels.describe()

	#print hotels_sort_location.groupby('NACIONALITY').NoOpinionsHotels.apply(lambda x: x.mean())

	hotels_sort_location[["NACIONALITY","RATING"]].groupby("NACIONALITY").agg([('average','mean'),('range',lambda x:x.max()-x.min())]).plot(kind='bar'); plt.axhline(0, color='k')
	plt.figure()
	#print hotels_sort_location[["NACIONALITY","RATING"]].groupby("NACIONALITY").agg([('average','mean'),('range',lambda x:x.max()-x.min())])



if __name__ == '__main__':
	get_graphics_hotels("../data/TripAdvisor/pdata_hotel_categorizado_com.csv")