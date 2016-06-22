__author__ = 'cesar17'

import json
import re

def get_fields_tw():
    tw_file = open('../data/tweets_file.csv', 'w')
    cabecera = 'timestamp_ms,userId,longitude,latitude,texto,language,favorite_count\n'
    tw_file.write(cabecera)
    data = open('text.json')
    # Cada line es un objeto json
    for line in data:
        tweet = json.loads(line)
        longitude = str(tweet['coordinates']['coordinates'][0])     # lo que esta entre llaves representa el key y lo que retorna es el value  K
        latitude = str(tweet['coordinates']['coordinates'][1])
        texto = tweet['text']
        texto = re.sub(r'@(.+?)\s+', '', texto)
        texto = re.sub(r'#(.+?)\s+', '', texto)
        texto = re.sub(r'http(.+?)\s+', '', texto)
        texto = re.sub(r'http(.+?)\Z', '', texto)
        print texto
        print '----'
        line = tweet['id_str'] + ',' + longitude + ',' + latitude + ',' + texto + ',' + tweet['created_at'] + '\n'
        #print line
    tw_file.close()
    data.close()

if __name__ == '__main__':
    get_fields_tw()