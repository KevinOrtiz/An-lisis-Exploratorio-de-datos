# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 23:37:05 2016

@author: made
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.cm as cmx
import matplotlib.colors as colors
import pandas as pd


    
##-78.5906982422,-0.3968779297,-78.2968139648,0.0082397461
def main():   
    file_dir = '../../data/Words/PalabrasSustantivos.csv'
    
    df = pd.read_csv(file_dir)

    
    fig = plt.figure(figsize=(20,10))   
    themap = Basemap(projection='gall',
                  llcrnrlon = 0.0082397461,              # lower-left corner longitude
                  llcrnrlat = -78.2968139648,               # lower-left corner latitude
                  urcrnrlon = -0.3968779297,               # upper-right corner longitude
                  urcrnrlat = -78.5906982422,               # upper-right corner latitude
                  resolution = 'l',
                  )
        
    themap.drawmapboundary(fill_color='white')
    
    x, y = themap(df['longitude'].values, df['latitude'].values)
        
    themap.scatter(x, 
                   y, 
                   s = 5, 
                   c= 'r', 
                   marker = 'o', 
                   color = df['colors'].values, 
                   alpha = 1.0)
    """themap.plot(x, y, 
                'o',                    # marker shape
                color= df['colors'].values,         # marker colour
                markersize=3            # marker size
                )
    """
    plt.show()
    
if __name__=='__main__':
    main()  