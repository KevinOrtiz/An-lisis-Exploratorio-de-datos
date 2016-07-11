__author__ = 'cesar17'
from wordcloud import WordCloud
import pandas as pd


def descriptive_stats():
    tweets_df = pd.read_csv("../data/Twitter/tweets_depurated_bboxes.csv", index_col=False)
    poi_cosas_nTw =  pd.read_csv('../data/Twitter/poi_cosas_hacer_nTw.csv')
    size = str(len(tweets_df.index))
    print 'Total de tweets geolocalizados en el dataset:  ' + size
    print '---'
    print 'Total de tweets alrededor de POIs:  '
    print 'Descripcion de tweets alrededor de los POIs'
    print poi_cosas_nTw['n_tw'].describe()


def get_wordCloud(from_poi_file_csv):
    tw_cat_a = open(from_poi_file_csv)
    text = ''
    hashtags = ''
    for line in tw_cat_a:
        line = line.strip()
        aux = line.split(',')
        if aux[4] == 'es':
            words = aux[3].split('&')
            htags = aux[7].split('&')
            for w in words:
                if len(w) >= 3:
                    text = text + w + ' '
            text = text + '\n'
            for h in htags:
                if h != '-':
                    hashtags = hashtags + h + ' '
                    # hashtags = hashtags + '\n'

    print hashtags
    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt

    plt.imshow(wordcloud)
    plt.title('Word Cloud Texto')
    plt.axis("off")
    # take relative word frequencies into account, lower max_font_size
    # wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(ha)
    wordcloud = WordCloud().generate(hashtags)
    plt.figure()
    plt.title('Word Cloud Hastags')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    descriptive_stats()
    # get_wordCloud('../data/Twitter/tw_cosas_hacer_a.csv')
