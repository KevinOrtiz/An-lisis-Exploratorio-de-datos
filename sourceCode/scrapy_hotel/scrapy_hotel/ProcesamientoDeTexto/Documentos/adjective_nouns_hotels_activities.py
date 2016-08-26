import json as js
import io
import re
import os
import string
#import hunspell
import unicodedata
import nltk
import unidecode

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

local_stopwords = ['quito', 'ecuador', 'pichincha', 'quitoecuador', 'ecuadorquito', 'post', 'photo']

cachedStopWordsEnglish = stopwords.words("english")
cachedStopWordsSpanish = stopwords.words("spanish")
nouns = []
adjectives = []

"""
Funcion:        create_feature_file_hotels
Autor:          Jose Velez Gomez
Descripcion:    Crea una lista de los feature(nouns y adjective) de los reviews
Estado:         Terminado
"""
def create_feature_file_hotels(input_file, output_file, dominio):

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)

	for element in data_json:
		if element['location_hotel'][0] is not None and element['location_hotel'][1] is not None:
			filename_hotel = put_name_corpus(element['name_hotel'], output_file)

			if element['reviews_hotel']:
				#Creacion del archivo text
				csv_file_adjective = create_file('Hoteles/Adjectives', dominio, filename_hotel, 'csv', 'adjectives')
				csv_file_nouns = create_file('Hoteles/Nouns', dominio, filename_hotel, 'csv', 'nouns')
				cabecera_csv = 'Reviews\n'			#Creo la cabecera del CSV
				csv_file_adjective.write(cabecera_csv)
				csv_file_nouns.write(cabecera_csv)

				list_nouns = list_adjectives = []

				for review in element['reviews_hotel']:
					if review:
						for text in review['description_review']:
							if text:
								text = clean_text(text)
								text = clean_text_stopwords(text, dominio)
								list_text_pos_tag = create_list_tokenization(text)
								adjectives = get_adjectives(list_text_pos_tag)
								nouns = get_nouns(list_text_pos_tag)
								list_nouns = list_nouns + nouns
								list_adjectives = list_adjectives + adjectives
				csv_file_adjective.write(unicode(js.dumps(list_adjectives, ensure_ascii=False)))
				csv_file_nouns.write(unicode(js.dumps(list_nouns, ensure_ascii=False)))
				csv_file_adjective.close()
				csv_file_nouns.close()


"""
Funcion:        create_documents_activities
Autor:          Jose Velez Gomez
Descripcion:    
Estado:         Terminado
"""
def create_feature_file_activities(input_file, output_file, dominio):

	with open(input_file) as dataFile: #File in  en Spanish
			data_json = js.load(dataFile)
					
	for element in data_json:
		if element['location_actividad'][0] is not None and element['location_actividad'][1] is not None:
			filename_actividad = put_name_corpus(element['name_actividad'], output_file)

			if element['reviews_actividad']:
				#Creacion del archivo text
				csv_file_adjective = create_file('Actividades/Adjectives', dominio, filename_actividad, 'csv', 'adjectives')
				csv_file_nouns = create_file('Actividades/Nouns', dominio, filename_actividad, 'csv', 'nouns')
				cabecera_csv = 'Reviews\n'			#Creo la cabecera del CSV
				csv_file_adjective.write(cabecera_csv)
				csv_file_nouns.write(cabecera_csv)

				list_nouns = list_adjectives = []

				for review in element['reviews_actividad']:
					if review:
						for text in review['description_review']:
							if text:
								text = clean_text_stopwords(text,dominio)
								list_text_pos_tag = create_list_tokenization(text)
								adjectives = get_adjectives(list_text_pos_tag)
								nouns = get_nouns(list_text_pos_tag)
								list_nouns = list_nouns + nouns
								list_adjectives = list_adjectives + adjectives
				csv_file_adjective.write(unicode(js.dumps(list_adjectives, ensure_ascii=False)))
				csv_file_nouns.write(unicode(js.dumps(list_nouns, ensure_ascii=False)))
				csv_file_adjective.close()
				csv_file_nouns.close()


def get_nouns(list_text_pos_tag):
	NN = ['NN', 'NNP', 'NNS']
	nouns  = []
	nouns = [tupla[0] for tupla in list_text_pos_tag if ((tupla[1] in NN) and (tupla[1] not in local_stopwords)) ]
	
	return nouns


def get_adjectives(list_text_pos_tag):
	JJ = ['JJ','JJR','JJS']
	adjectives = []
	adjectives = [tupla[0] for tupla in list_text_pos_tag if ((tupla[1] in JJ) and (tupla[1] not in local_stopwords)) ]

	return adjectives


def put_name_corpus(name_place, output_file):

	name_place = string.replace(name_place, " ", '_')
	name_place = clean_text(name_place)
	filename = output_file+'_'+name_place

	return filename


def create_file(folder,dominio, filename, folder_extension, type_feature):

	name_hotel = str(folder+'/'+dominio+'/'+type_feature+'_'+filename+'.'+folder_extension)
	return  open(''+name_hotel,'w')


def deleteConsecutives(word):
	if re.search(r'(.)\1\1', word):
		prev1 = ''
		prev2 = ''
		result = ''
		for ch in word:
			if (ch != prev1 and ch != prev2):
				if (prev2 != ''):
					prev2 = prev1
					prev1 = ch
					result=result+ch
				else:
					prev1 = ch
					result = result + ch
		return result
	else:
		return word


def remove_accents(input_text):
	nkfd_form = unicodedata.normalize('NFKD', unicode(input_text))
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def create_list_tokenization(input_text):
	#Tokenization de review
	objectToken = TweetTokenizer(strip_handles=True, reduce_len=True)
	text_tokenizado = objectToken.tokenize(input_text)
	list_tokenization_text = nltk.pos_tag(text_tokenizado)
	return list_tokenization_text


def clean_text_stopwords(input_text, dominio):
	#convert to lower
	input_text = input_text.lower()
	#remove accents 
	input_text = remove_accents(input_text)
	#remove repeated chararter 
	input_text = deleteConsecutives(input_text)
	#stopwords del corpus general y de la lsita ['quito', 'ecuador', 'pichincha', 'quitoecuador', 'ecuadorquito', 'post', 'photo']
	if dominio == 'co':
		input_text = ' '.join([word for word in input_text.split() if( word not in cachedStopWordsSpanish and word not in local_stopwords)])
	else:
		input_text = ' '.join([word for word in input_text.split() if( word not in cachedStopWordsEnglish and word not in local_stopwords)])
	
	return input_text


def clean_text(input_text):
	input_text = re.sub('[0123456789!@#$%&/()=?].:,;', '', input_text)
	return input_text


if __name__ == '__main__':
	print "HOTELES CO"
	create_feature_file_hotels("../dataset/data_set_hotels_location_co.json", 'hotels_co', 'co')
	print "HOTELES COM"
	create_feature_file_hotels("../dataset/data_set_hotels_location_com.json", 'hotels_com', 'com' )
	print "ACTIVIDADES CO"
	create_feature_file_activities("../dataset/data_set_activities_location_co.json",'activities_co', 'co')
	print "ACTIVIDADES COM"
	create_feature_file_activities("../dataset/data_set_activities_location_com.json",'activities_com', 'com')