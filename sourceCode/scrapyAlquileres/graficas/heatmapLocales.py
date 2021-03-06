import plotly.plotly as py
import pandas as pd

df = pd.read_csv('Alquiler_col_influyente.csv')
df.head()

scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

data = [ dict(
        type = 'scattergeo',
        locationmode = 'Ecuador',
        lon = df['longitude'],
        lat = df['latitude'],
        mode = 'markers',
        marker = dict( 
            size = 8, 
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = scl,
            cmin = 0,
            colorbar=dict(
                title="Opinion sobre restaurantes en los ultimos 5 anos"
            )
        ))]

layout = dict(
        title = 'Opiniones de los restaurantes ',
        colorbar = True,   
        geo = dict(
            scope='usa',
            #projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5        
        ),
    )

fig = dict( data=data, layout=layout )
url = py.plot( fig, validate=False, filename='Grafica-Restaurantes_locales' )