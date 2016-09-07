__author__ = 'madevelasco'

import pandas as pd

#IntinanMuseum
#LaVirginlPanecillo
#MuseoMindae
#MuseoSanAgustin
#ParqueLaCarolina

place = "ParqueLaCarolina"
path_open = "../data/Twitter/tw_cosas_hacer_"+place+".csv"
path_result = "../data/Twitter/"+place+".csv"

result = pd.read_csv(path_open, sep=',')
local_stopwords = ['quito', 'ecuador', 'pichincha', 'quitoecuador', 'ecuadorquito', '', 'post', 'photo']

def removestop(x):
    words = x.split('&')
    res = ''
    for word in words:
        if word not in local_stopwords:
            res = res + "&"+ word
    return res

result['dep'] = result['words'].apply(removestop)

result.to_csv(path_result, sep=',', encoding='utf-8')