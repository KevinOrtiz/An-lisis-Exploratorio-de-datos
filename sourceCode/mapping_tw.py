__author__ = 'madevelasco'

#Based on http://qingkaikong.blogspot.com/2016/02/plot-earthquake-heatmap-on-basemap-and.html

import gmplot
import pandas as pd

tweet_path = '../data/Twitter/quito.csv'
heapmap_path = '../data/Twitter/tweets_heatmap.html'
scatter_path = '../data/Twitter/tweets_scatter.html'

tweets = pd.read_csv(tweet_path)
lats = tweets['latitude']
lons = tweets['longitude']
# tokens = tweets['words', 'lang']
# tokens.to_csv('raw.csv')
#Center of the map and zoom
gmap = gmplot.GoogleMapPlotter(-0.2324668, -78.4558138, 11)
gmap.heatmap(lats, lons)
gmap.draw(heapmap_path)

#gmap.plot(lats, lons, 'cornflowerblue', edge_width=10)
#gmap.scatter(lats, lons, '#3B0B39', size=40, marker=False)

gmap = gmplot.GoogleMapPlotter(-0.2324668, -78.4558138, 11)
gmap.scatter(lats, lons, '#3B0B39', size=40, marker=False)
gmap.draw(scatter_path)