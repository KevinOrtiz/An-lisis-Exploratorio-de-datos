__author__ = 'cesar17'
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt


def descriptive_stats():
    tweets_df = pd.read_csv("../data/Twitter/tweets_depurated_bboxes.csv", index_col=False)
    poi_cosas_nTw =  pd.read_csv('../data/Twitter/poi_cosas_hacer_nTw.csv')
    size = str(len(tweets_df.index))
    n_users = str(tweets_df['id_str'].nunique())
    print 'Total de tweets geolocalizados en el dataset:  ' + size
    print 'Total de usuarios unicos:   ' + n_users
    print '---'
    print 'Total de tweets alrededor de POIs:  ' + str(poi_cosas_nTw['n_tw'].sum())
    print 'Descripcion de tweets alrededor de los POIs'
    print poi_cosas_nTw['n_tw'].describe()
    tweets_df = tweets_df[tweets_df['bbox_cosas_hacer'] != '-']
    gb_tweets_df = tweets_df[['id_str', 'isDay', 'isWeekDay', 'bbox_cosas_hacer']].groupby('bbox_cosas_hacer')
    # Plot number of tweets
    nTw_poi = gb_tweets_df.size()
    nTw_poi = nTw_poi.sort_values(ascending=False).head(10)
    print '***** Number of tweets top POI *****'
    print nTw_poi
    # my_plot = nTw_poi.plot(kind='bar',legend=None,title="Number of tweets in the POIs")
    # my_plot.set_xlabel("Points of Interest")
    # my_plot.set_ylabel("Number of tweets")
    # plt.show()
    # ##

    gb_uniq_user_tweets = gb_tweets_df['id_str'].apply(lambda x: len(x.unique()))
    gb_uniq_user_tweets = gb_uniq_user_tweets.sort_values(ascending=False).head(5)
    print '***** Number of twitter users at POIs *****'
    print gb_uniq_user_tweets
    my_plot = gb_uniq_user_tweets.plot(kind='bar',legend=None,title="Number of twitter users at POIs")
    my_plot.set_xlabel("Points of Interest")
    my_plot.set_ylabel("Number Users")
    plt.show()



def get_wordCloud(from_poi_file_csv):
    local_stopwords = ['quito', 'ecuador', 'pichincha', 'quitoecuador', 'ecuadorquito', 'post', 'photo', 'dia', 'hoy', 'mas', 'uio']
    tw_cat_a = open(from_poi_file_csv)
    from_poi_file_csv = from_poi_file_csv.replace('.csv', '')
    lugar = from_poi_file_csv.split('/')[4].split('_')[3]
    text = ''
    hashtags = ''
    for line in tw_cat_a:
        line = line.strip()
        aux = line.split(',')
        if aux[4] == 'es':
            words = aux[3].split('&')
            htags = aux[7].split('&')
            for w in words:
                w = w.lower()
                if w not in local_stopwords and len(w)>=3:
                    text = text + w + ' '
            text = text + '\n'
            for h in htags:
                if h != '-':
                    h = h.lower()
                    if h not in local_stopwords:
                        hashtags = hashtags + h + ' '
                    # hashtags = hashtags + '\n'

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:

    plt.imshow(wordcloud)

    titulo = 'Word Cloud Tweets' + ' - ' + lugar
    plt.title(titulo)
    plt.axis("off")
    # # take relative word frequencies into account, lower max_font_size
    # # wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(ha)
    # if hashtags:
    #     wordcloud = WordCloud().generate(hashtags)
    # plt.figure()
    # titulo = 'Word Cloud Hashtags' + ' - ' + lugar
    # plt.title(titulo)
    # plt.imshow(wordcloud)
    # plt.axis("off")
    plt.show()


if __name__ == '__main__':
    descriptive_stats()
    file_rutas = ['../data/Twitter/tws_alrededor_poi/tw_cosas_hacer_MuseoMindae.csv', '../data/Twitter/tws_alrededor_poi/tw_cosas_hacer_IntinanMuseum.csv',
                  '../data/Twitter/tws_alrededor_poi/tw_cosas_hacer_LaVirginlPanecillo.csv', '../data/Twitter/tws_alrededor_poi/tw_cosas_hacer_MuseoSanAgustin.csv',
                  '../data/Twitter/tws_alrededor_poi/tw_cosas_hacer_ParqueLaCarolina.csv']
    # for ruta in file_rutas:
    #     get_wordCloud(ruta)
    # get_wordCloud('../data/Twitter/tws_alrededor_poi/tw_cosas_hacer_LaVirginlPanecillo.csv')
