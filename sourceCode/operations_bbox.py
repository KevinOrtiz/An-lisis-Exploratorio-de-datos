__author__ = 'cesar17'
from geolocation_bbox import GeoLocation
import pandas as pd
import re

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
            return key
    return '-'

def set_bbox_top_cosas_hacer():
    # a Iglesia de la compania de jesus
    # b Teleferico de quito
    # sitios = {'a': [-78.51385, -0.221065], 'b': [-78.51503, -0.223030]}
    sitios = get_pois_location_trip_advisor('../data/TripAdvisor/nuevo_data_actividades.csv')
    bboxes = {}
    for key, value in sitios.iteritems():
        longitude = value[0]
        latitude = value[1]
        loc = GeoLocation.from_degrees(latitude, longitude)
        distance = 0.2  # 1 kilometer
        SW_loc, NE_loc = loc.bounding_locations(distance)
        minlong = SW_loc.deg_lon
        minlat = SW_loc.deg_lat
        maxlong = NE_loc.deg_lon
        maxlat = NE_loc.deg_lat
        bboxes[key] = [minlong, minlat, maxlong, maxlat]
    print bboxes
    # tweets_df = pd.read_csv("../data/Twitter/tweets_depurated.csv", index_col=False)
    # tw_aux = tweets_df[['longitude','latitude']]
    # tweets_df['bbox_cosas_hacer'] = tw_aux.apply(lambda x: get_index_bbox(x, bboxes), axis=1)
    # poi_cosas_hacer_df = pd.DataFrame(columns=('poi_name', 'n_tw'))
    # index_poi = 0
    # for key in bboxes.iterkeys():
    #     tw_cosas_hacer_lugar = tweets_df[tweets_df['bbox_cosas_hacer']==key]
    #     size = len(tw_cosas_hacer_lugar.index)
    #     poi_cosas_hacer_df.n_tw = poi_cosas_hacer_df.n_tw.astype(int)
    #     poi_cosas_hacer_df.loc[index_poi] = [key, size]
    #     index_poi += 1
    #     if not tw_cosas_hacer_lugar.empty:
    #         filename = '../data/Twitter/tws_alrededor_poi/tw_cosas_hacer_' + key + '.csv'
    #         tw_cosas_hacer_lugar.to_csv(filename, index=False)
    # poi_cosas_hacer_df = poi_cosas_hacer_df.sort_values(by='n_tw', ascending=False)
    # print '*** Top5 de los POIs considerando el numero de tweets***'
    # top_poi_cosas_hacer = poi_cosas_hacer_df.head(5)
    # print top_poi_cosas_hacer
    # poi_cosas_hacer_df.to_csv('../data/Twitter/poi_cosas_hacer_nTw.csv', index=False)
    # tweets_df.to_csv('../data/Twitter/tweets_depurated_bboxes.csv', index=False)

def get_pois_location_trip_advisor(category_csv_file):
    sitios = {}
    dataframe = pd.read_csv(category_csv_file)
    dataframe = dataframe[['name', 'longitude', 'latitude']]
    for itr in dataframe.itertuples():
        name = itr[1]
        name = name.replace(' ', '')
        name = re.sub(r'de', '', name)
        name = re.sub(r'del', '', name)
        name = re.sub(r'la', '', name)
        name = re.sub(r'of', '', name)
        longitude = round(itr[2], 7)
        latitude = round(itr[3], 7)
        sitios[name] = [longitude, latitude]
    return sitios


if __name__ == '__main__':
    set_bbox_top_cosas_hacer()