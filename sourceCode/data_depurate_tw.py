# -*- coding: utf-8 -*-

__author__ = 'madevelasco'

import json
import re
import unicodedata
import hunspell
import sys
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def get_fields_tw():
    tw_file = open('../data/Twitter/tweets_depurated.csv', 'w')
    tw_file_no_text = open('../data/Twitter/tweets_depurated_noText.csv', 'w')
    cabecera = 'id_str,longitude,latitude,words,lang,timestamp_ms,n_retw,hashtags\n'
    cabecera_no_text = 'id_str,longitude,latitude,lang,timestamstamp_ms,n_retw\n'
    tw_file.write(cabecera)
    tw_file_no_text.write(cabecera_no_text)
    #Reemplazar por nombre archivo
    # data = open('text.json')
    # Cada line es un objeto json
    for line in sys.stdin:
        line = line
        if (line.strip() != '\n'):
            hashtags = ''
            try:
                tweet = json.loads(line)
                if tweet['coordinates']:
                    longitude = str(tweet['coordinates']['coordinates'][0])
                    latitude = str(tweet['coordinates']['coordinates'][1])
                    texto = tweet['text']
                    texto = re.sub(r'@(.+?)\s+', '', texto)
                    texto = re.sub(r'@(.+?)\Z', '', texto)
                    texto = re.sub(r'#(.+?)\s+', '', texto)
                    texto = re.sub(r'#(.+?)\Z', '', texto)
                    texto = re.sub(r'http(.+?)\s+', '', texto)
                    texto = re.sub(r'http(.+?)\Z', '', texto)
                    texto = re.sub(r'jaja{1,}?', '', texto)
                    texto = re.sub(r'j{2,}?', '', texto)
                    texto = re.sub(r'jeje{1,}?', '', texto)
                    content = normalization(texto, tweet['lang'])
                    #No devuelve tweet si está vacío tras normalizar y eliminar stopwords
                    if (content != "" and len(content)>=3):
                        for h in tweet['entities']['hashtags']:
                            hashtags = hashtags + '&' + h['text'].encode('ascii','ignore')
                        if not hashtags:
                            hashtags = '-'
                        line = tweet['id_str'] + ',' + longitude + ',' \
                               + latitude + ',' + content + ',' + tweet['lang']+','+ tweet['timestamp_ms']\
                               + ',' + str(tweet['retweet_count']) + ',' + hashtags + '\n'
                        tw_file.write(line)
                    line_noText = tweet['id_str'] + ',' + longitude + ',' \
                               + latitude + ',' + tweet['lang']+','+ tweet['timestamp_ms']\
                               + ',' + str(tweet['retweet_count']) + '\n'
                    tw_file_no_text.write(line_noText)

            except ValueError:
                print 'Decoding JSON has failed'
    tw_file.close()

def normalization(text, lang):
    text = text.lower()
    other = ''
    hobj_spanish = hunspell.HunSpell('dic_spanish/Spanish.dic', 'dic_spanish/Spanish.aff')
    stemmer_english = SnowballStemmer("english")
    for element in text:
        other =other+remove_accents(element)
    text = other

    words = re.findall(r'\w+', text, flags=re.UNICODE | re.LOCALE)
    depured = ""
    for word in words:
        #Depuración de acuerdo al idioma
        if lang == "en":
            if word not in stopwords.words('english'):
                word = stemmer_english.stem(word)
                depured = depured+"&"+word
        else:
            if word not in stopwords.words('spanish'):
                stem = hobj_spanish.stem(word)
                if stem:
                    word = stem[0]
                depured = depured + "&" + word

    return depured

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

if __name__ == '__main__':
    get_fields_tw()