# -*- coding: utf-8 -*-

import matplotlib.cm as cmx
import matplotlib.colors as colors
import pandas as pd
import matplotlib.cm as cm
import numpy as np 
"""
Created on Wed Aug 17 11:51:29 2016

@author: Administrator
"""

def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color
    
def main():  
    file_dir = '../../data/Words/PalabrasSustantivos.csv'
    file_name = '../../data/Words/PalabrasSustantivosColored.csv'
    
    df = pd.read_csv(file_dir)
    cmap = get_cmap (len(df['word'].unique()))
    
    colors = cm.rainbow(np.linspace(0, 1, len(df['word'].unique())))
    print(colors)
    
    df['colors'] = ''
    prev = df['word'].iloc[0]
    i = 0
    
    for index , row in df.iterrows():
        if (prev == df.loc[index, 'word']):
            df.loc[index, 'colors'] = cmap(i)
        else:
            prev = df.loc[index, 'word']
            i+=1
            df.loc[index, 'colors'] = cmap(i)
            
            
    df.to_csv(file_name, sep=',', encoding='utf-8')

if __name__=='__main__':
    main()  
    