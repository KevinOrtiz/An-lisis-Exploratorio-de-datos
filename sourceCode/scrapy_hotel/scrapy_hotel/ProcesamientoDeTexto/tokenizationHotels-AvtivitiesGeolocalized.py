import json as js
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import io


"""
Funcion:        token_hotels
Autor:          Jose Velez Gomez
Descripcion:    Tokenization hotels in Spanish -- English
Estado:         Terminado
"""
def token_hotels():
	#with open("../spiders/data_set_hotel_com.json") as dataFile: #File in  English
	with open("../spiders/data_set_hotel_co.json") as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	lista_Reviews = {}
	lista_comentarios = []
	contador = 0
	with io.open('FileTokenizationHotelsGeolocalizedSpanish.text','w',encoding='utf-8') as file_tokenization:
		for element in data_json:
			lista_comentarios = []
			if element['location_hotel'][0] is not None and element['location_hotel'][1] is not None:
				contador = contador + 1
				for review in element['reviews_hotel']:
					if ('description_review' in review):
						for text in review['description_review']:
							objectToken = TweetTokenizer(strip_handles=True, reduce_len=True)
							text = ' '.join([word for word in text.split() if word not in stopwords.words("spanish")])
							#text = ' '.join([word for word in text.split() if word not in stopwords.words("english")])
							reviews_tokenizado = objectToken.tokenize(text)
							lista_comentarios.append(reviews_tokenizado)
					break
				lista_Reviews['name_hotel'] = element['name_hotel']
				lista_Reviews['location_hotel'] = [element['location_hotel'][0], element['location_hotel'][1]]
				lista_Reviews['reviews'] = lista_comentarios
				lista_Reviews['indice'] = contador
				del lista_comentarios
				file_tokenization.write(unicode(js.dumps(lista_Reviews, ensure_ascii=False)))
	file_tokenization.close()

"""
Funcion:        token_activities
Autor:          Jose Velez Gomez
Descripcion:    Tokenization activities in Spanish -- English
Estado:         Terminado
"""
def token_activities():
	#with open("../spiders/data_set_actividades_com.json") as dataFile: #File in  English
	with open("../spiders/data_set_actividades_co.json") as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	lista_Reviews = {}
	lista_comentarios = []
	contador = 0
	with io.open('FileTokenizationActivitiesGeolocalizedSpanish.text','w',encoding='utf-8') as file_tokenization:
		for element in data_json:
			lista_comentarios = []
			if element['location_actividad'][0] is not None and element['location_actividad'][1] is not None:
				contador = contador + 1
				for review in element['reviews_actividad']:
					if ('description_review' in review):
						for text in review['description_review']:
							objectToken = TweetTokenizer(strip_handles=True, reduce_len=True)
							text = ' '.join([word for word in text.split() if word not in stopwords.words("spanish")])
							#text = ' '.join([word for word in text.split() if word not in stopwords.words("english")])
							reviews_tokenizado = objectToken.tokenize(text)
							lista_comentarios.append(reviews_tokenizado)
					break
				lista_Reviews['name_actividad'] = element['name_actividad']
				lista_Reviews['location_actividad'] = [element['location_actividad'][0], element['location_actividad'][1]]
				lista_Reviews['reviews'] = lista_comentarios
				lista_Reviews['indice'] = contador
				del lista_comentarios
				file_tokenization.write(unicode(js.dumps(lista_Reviews, ensure_ascii=False)))
	file_tokenization.close()


if __name__ == '__main__':
	token_hotels()
	token_activities()