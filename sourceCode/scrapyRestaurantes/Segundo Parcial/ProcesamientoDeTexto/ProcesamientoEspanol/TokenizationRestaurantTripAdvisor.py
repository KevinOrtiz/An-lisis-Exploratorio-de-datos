import json as js
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import io

with open("salidaRestaurantePrueba.json") as dataFile:
        datas = js.load(dataFile)
        lista_Reviews = {}
        lista_comentarios = []
        for i in datas:
            if i['posicion'][0] is not None and i['posicion'][1] is not None:
                for y in i['itemsReviews']:
                    if ('comentarios' in y):
                        objectToken = TweetTokenizer(strip_handles=True,reduce_len=True)
                        for text in y['comentarios']:
                            text = ' '.join([word for word in text.split() if word not in stopwords.words("spanish")])
                            reviews_tokenizado =objectToken.tokenize(text)
                            lista_comentarios.append(reviews_tokenizado)
                        lista_Reviews['name'] = i['tituloLugar']
                        print lista_Reviews['name']
                        lista_Reviews['posicion'] = [i['posicion'][0],i['posicion'][1]]
                        lista_Reviews['reviews'] = lista_comentarios


with io.open('ArchivoTokenizadoRestaurantesGeolocalizados.text','w',encoding='utf-8') as f:
    f.write(unicode(js.dumps(lista_Reviews, ensure_ascii=False)))
f.close()












