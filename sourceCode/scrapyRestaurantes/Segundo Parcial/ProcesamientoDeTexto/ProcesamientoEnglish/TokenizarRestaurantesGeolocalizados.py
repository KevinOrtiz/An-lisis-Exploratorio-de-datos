import json as js
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import io
import nltk

with open("salidaRestaurantes_versionCOM.json") as dataFile:
        datas = js.load(dataFile)

lista_Reviews = {}
contador = 0
with io.open('ArchivoTokenizadoRestaurantesGeolocalizadosEnglish.text','w',encoding='utf-8') as f:
    for i in datas:
        lista_comentarios = []
        if i['posicion'][0] is not None and i['posicion'][1] is not None:
            contador =contador + 1
            for y in i['itemsReviews']:
                if ('comentarios' in y):
                    for text in y['comentarios']:
                        objectToken = TweetTokenizer(strip_handles=True, reduce_len=True)
                        text = ' '.join([word for word in text.split() if word not in stopwords.words("spanish")])
                        reviews_tokenizado = objectToken.tokenize(text)
                        lista_comentarios.append(nltk.pos_tag(reviews_tokenizado))
                break
            lista_Reviews['name'] = i['tituloLugar']
            lista_Reviews['posicion'] = [i['posicion'][0], i['posicion'][1]]
            lista_Reviews['reviews'] = lista_comentarios
            lista_Reviews['indice'] = contador
            del lista_comentarios
            f.write(unicode(js.dumps(lista_Reviews, ensure_ascii=False)))
f.close()












