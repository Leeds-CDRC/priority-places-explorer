from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import json

app = Dash(__name__)
server=app.server

app.layout = html.Div([
    html.H4('Priority Places'),
    html.P("Select a domain:"),
    dcc.RadioItems(
        id='domain', 
        options=["Combined", "Proximity to non-supermarkets"],
        value="Combined",
        inline=True
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("domain", "value"))
def display_choropleth(domain):
    df = pd.read_csv('/data/Retailers - other_1km_count.csv')
    lsoa_centroids = pd.read_csv('data/Lower_layer_Super_Output_Areas_(December_2011)_Population_Weighted_Centroids_WGS.csv')
    df_joined = df.merge(lsoa_centroids, left_on='lsoa11cd', right_on='lsoa11cd')
    df_joined['logFHRSID'] = np.log10(1+df_joined['FHRSID'])
    fig = px.scatter_mapbox(
                        df_joined, 
                        lat='latitude',
                        lon='longitude', 
                        color='logFHRSID', 
                        hover_name='lsoa11cd', 
                        hover_data=['lsoa11nm', 'FHRSID'],
                        range_color=[0,2.5], 
                        height=600, 
                        color_continuous_scale='viridis', 
                        center={'lat': 53.8067, 'lon': -1.5550})
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    fig.update_geos(fitbounds="locations", visible=True)
    return fig

if __name__=="__main__":
    app.run(host='0.0.0.0',
            port='8000',
            debug=True)