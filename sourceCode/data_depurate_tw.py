# -*- coding: utf-8 -*-

__author__ = 'madevelasco'

import json
import re
import unicodedata
from nltk.corpus import stopwords

def get_fields_tw():
    tw_file = open('../data/Twitter/tweets_file.csv', 'w')
    cabecera = 'id_str,userId,longitude,latitude,words, lang, timestamp_ms \n'
    tw_file.write(cabecera)
    #Reemplazar por nombre archivo
    data = open('tweets170616.json')
    # Cada line es un objeto json
    for line in data:
        line = line
        if (line.strip() != '\n'):
            try:
                tweet = json.loads(line)
                longitude = str(tweet['coordinates']['coordinates'][0])
                latitude = str(tweet['coordinates']['coordinates'][1])
                texto = tweet['text']
                texto = re.sub(r'@(.+?)\s+', '', texto)
                texto = re.sub(r'#(.+?)\s+', '', texto)
                texto = re.sub(r'http(.+?)\s+', '', texto)
                texto = re.sub(r'http(.+?)\Z', '', texto)
                content = normalization(texto, tweet['lang'])
                #No devuelve tweet si está vacío tras normalizar y eliminar stopwords
                if (content != ""):
                    line = tweet['id_str'] + ',' + str(tweet['user']['id'])+','+ longitude + ',' \
                           + latitude + ',' + content + ',' +tweet['lang']+','+ tweet['timestamp_ms'] + '\n'
                    tw_file.write(line)
            except ValueError:
                print 'Decoding JSON has failed'
    tw_file.close()
    data.close()

def normalization(text, lang):
    text = text.lower()
    other = ''
    for element in text:
        other =other+remove_accents(element)
    text = other

    words = re.findall(r'\w+', text, flags=re.UNICODE | re.LOCALE)
    depured = ""
    for word in words:
        #Depuración de acuerdo al idioma
        if lang == "en":
            if word not in stopwords.words('english'):
                depured = depured+"&"+word
        else:
            if word not in stopwords.words('spanish'):
                depured = depured + "&" + word

    return depured

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

if __name__ == '__main__':
    get_fields_tw()