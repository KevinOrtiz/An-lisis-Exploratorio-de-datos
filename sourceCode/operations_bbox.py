__author__ = 'cesar17'
from geolocation_bbox import GeoLocation
import pandas as pd
from wordcloud import WordCloud

def is_in_bounding_box(location, bbox):
    longitud= location[0]
    latitud = location[1]
    minLong = bbox[0]
    minLat = bbox[1]
    maxLong = bbox[2]
    maxLat = bbox[3]
    return longitud >= minLong and longitud <= maxLong and latitud >= minLat and latitud <= maxLat

def get_index_bbox(location, bboxes):
    for key in bboxes.iterkeys():
        bbox = bboxes[key]
        if is_in_bounding_box(location, bbox):
            # print key
            return key
        else:
            return '-'

def set_bbox_top_cosas_hacer():
    # a Iglesia de la compania de jesus
    # b Teleferico de quito
    sitios = {'a': [-78.51385, -0.221065], 'b': [-78.51503, -0.223030]}
    bboxes = {}
    for key in sitios.iterkeys():
        value = sitios[key]
        longitude = value[0]
        latitude = value[1]
        loc = GeoLocation.from_degrees(latitude, longitude)
        distance = 1  # 1 kilometer
        SW_loc, NE_loc = loc.bounding_locations(distance)
        minlong = SW_loc.deg_lon
        minlat = SW_loc.deg_lat
        maxlong = NE_loc.deg_lon
        maxlat = NE_loc.deg_lat
        bboxes[key] = [minlong, minlat, maxlong, maxlat]

    tweets_df = pd.read_csv("../data/Twitter/tweets_depurated.csv")
    tw_aux = tweets_df[['longitude','latitude']]
    tweets_df['bbox_cosas_hacer'] = tw_aux.apply(lambda x: get_index_bbox(x, bboxes), axis=1)
    tw_cosas_hacer_cate = tweets_df[tweets_df['bbox_cosas_hacer']=='a']
    tw_cosas_hacer_cate.to_csv('../data/Twitter/tw_cosas_hacer_a.csv', index=False)
    tw_cosas_hacer_cate = tweets_df[tweets_df['bbox_cosas_hacer']=='b']
    tw_cosas_hacer_cate.to_csv('../data/Twitter/tw_cosas_hacer_b.csv', index=False)
    # aux = get_index_bbox([-79.8833,-2.1833], bboxes)
    # print aux

def get_wordCloud():
    tw_cat_a = open('../data/Twitter/tw_cosas_hacer_a.csv')
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

set_bbox_top_cosas_hacer()
get_wordCloud()