from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import json

app = Dash()
server = app.server

app.layout = html.Div([
    html.H4('Priority Places'),
    html.P("Select a domain:"),
    dcc.RadioItems(
        id='domain', 
        options=['domain_supermarket_proximity', 
                 'domain_supermarket_transport',
                 'domain_ecommerce_access', 
                 'domain_socio_demographic',
                 'domain_nonsupermarket_proximity', 
                 'domain_food_for_families',
                 'domain_fuel_poverty'],
        value="domain_supermarket_proximity",
        inline=True
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("domain", "value"))
def display_choropleth(domain):
    df = pd.read_csv('/data/priority_places_v0_1_ranked_domains_WGS.csv')
    fig = px.scatter_mapbox(
                        df, 
                        lat='latitude',
                        lon='longitude', 
                        color=domain, 
                        hover_name='geo_code', 
                        hover_data=['geo_code', domain],
                        range_color=[0,41728], 
                        height=600, 
                        color_continuous_scale='RdPu', 
                        center={'lat': 53.8067, 'lon': -1.5550})
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    fig.update_geos(fitbounds="locations", visible=True)
    return fig

if __name__=="__main__":
    app.run(debug=True)