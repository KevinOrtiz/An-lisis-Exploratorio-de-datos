import json as js
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import io
import nltk

cachedStopWordsEnglish = stopwords.words("english")
cachedStopWordsSpanish = stopwords.words("spanish")

"""
Funcion:        token_hotels
Autor:          Jose Velez Gomez
Descripcion:    Tokenization hotels in Spanish -- English
Estado:         Terminado
"""
def token_hotels(input_file, output_file, cachedStopWords):

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	lista_hotels = []
	lista_Reviews = {}
	lista_comentarios = []
	contador = 0
	with io.open(output_file,'w',encoding='utf-8') as file_tokenization:
		for element in data_json:
			lista_comentarios = []
			if element['location_hotel'][0] is not None and element['location_hotel'][1] is not None:
				contador = contador + 1
				for review in element['reviews_hotel']:
					if review:
						for text in review['description_review']:
							objectToken = TweetTokenizer(strip_handles=True, reduce_len=True)
							text = ' '.join([word for word in text.split() if word not in cachedStopWords])
							reviews_tokenizado = objectToken.tokenize(text)
							if reviews_tokenizado:
								lista = []
								for elem in reviews_tokenizado:
									if not (elem[0] == "." or elem[0] == "," or 
											elem[0] == ";" or elem[0] == ":" or 
											elem[0] == "?" or elem[0] == "!" or
											elem[0] == "(" or elem[0] == ")"):
										lista.append(elem)
								lista_comentarios.append(nltk.pos_tag(lista))
					
				lista_Reviews['name_hotel'] = element['name_hotel']
				lista_Reviews['location_hotel'] = [element['location_hotel'][0], element['location_hotel'][1]]
				lista_Reviews['reviews'] = lista_comentarios
				lista_Reviews['indice'] = contador
				lista_Reviews['rating_hotel'] = element['rating_hotel']
				del lista_comentarios
				lista_hotels.append(lista_Reviews)
				lista_Reviews = {}
		file_tokenization.write(unicode(js.dumps(lista_hotels, ensure_ascii=False)))
	file_tokenization.close()

"""
Funcion:        token_activities
Autor:          Jose Velez Gomez
Descripcion:    Tokenization activities in Spanish -- English
Estado:         Terminado
"""
def token_activities(input_file, output_file, cachedStopWords):

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	lista_activities = []
	lista_Reviews = {}
	lista_comentarios = []
	contador = 0
	with io.open(output_file,'w',encoding='utf-8') as file_tokenization:
		for element in data_json:
			lista_comentarios = []
			if element['location_actividad'][0] is not None and element['location_actividad'][1] is not None:
				contador = contador + 1
				for review in element['reviews_actividad']:
					if review:
						for text in review['description_review']:
							objectToken = TweetTokenizer(strip_handles=True, reduce_len=True)
							text = ' '.join([word for word in text.split() if word not in cachedStopWords])
							reviews_tokenizado = objectToken.tokenize(text)
							if reviews_tokenizado:
								lista = []
								for elem in reviews_tokenizado:
									if not (elem[0] == "." or elem[0] == "," or 
											elem[0] == ";" or elem[0] == ":" or 
											elem[0] == "?" or elem[0] == "!" or
											elem[0] == "(" or elem[0] == ")"):
										lista.append(elem)
								lista_comentarios.append(nltk.pos_tag(lista))
					
				lista_Reviews['name_actividad'] = element['name_actividad']
				lista_Reviews['location_actividad'] = [element['location_actividad'][0], element['location_actividad'][1]]
				lista_Reviews['reviews'] = lista_comentarios
				lista_Reviews['indice'] = contador
				lista_Reviews['rating_actividad'] = element['rating_actividad']
				del lista_comentarios
				lista_activities.append(lista_Reviews)
				lista_Reviews = {}
		file_tokenization.write(unicode(js.dumps(lista_activities, ensure_ascii=False)))
	file_tokenization.close()


if __name__ == '__main__':

	cachedStopWordsEnglish = stopwords.words("english")
	cachedStopWordsSpanish = stopwords.words("spanish")

	#token_hotels("data_set_hotels_location_co.json", 'tokens_hotels_co.text', cachedStopWordsSpanish)
	#token_hotels("data_set_hotels_location_com.json", 'tokens_hotels_com.text',cachedStopWordsEnglish )

	token_activities("data_set_activities_location_co.json",'tokens_activities_co.text', cachedStopWordsSpanish)
	token_activities("data_set_activities_location_com.json",'tokens_activities_com.text', cachedStopWordsEnglish)