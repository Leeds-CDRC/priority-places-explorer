from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import json

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(style={
                        'height': '100vh', 
                        'padding': 10
                      }, 
                      children=[
    
    html.H4('CDRC Priority Places'),
    #html.P("Select a domain:"),
    dcc.Dropdown(
        id='domain', 
        options=[{"label": "Combined Priority Places Index", "value": "combined"},
                 {"label": "Proximity to supermarket food retail facilities", "value": "domain_supermarket_proximity"}, 
                 {"label": "Accessibility to supermarket retail facilties", "value": "domain_supermarket_transport"}, 
                 {"label": "Access to online deliveries", "value": "domain_ecommerce_access"}, 
                 {"label": "Socio-demographic barriers", "value": "domain_socio_demographic"}, 
                 {"label": "Proximity to non-supermarket food retail facilities", "value": "domain_nonsupermarket_proximity"},
                 {"label": "Food support for families", "value": "domain_food_for_families"}, 
                 {"label": "Fuel poverty", "value": "domain_fuel_poverty"}],
        value='combined',
        multi=False,
        #style={'width': "100%"}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(), 

    dcc.Graph(id="graph", figure={}), 
    dcc.Markdown('''\nPriority Places is developed by the ESRC-funded [Consumer Data Research Centre](https://cdrc.ac.uk/) at the University of Leeds\n''')

])

@app.callback(
    Output("graph", "figure"), 
    Input("domain", "value"))
def display_choropleth(domain):
    df = pd.read_csv('/data/priority_places_v0_3_decile_domains_WGS.csv',
                     dtype={'domain_supermarket_proximity':'category',
                            'domain_supermarket_transport':'category',
                            'domain_ecommerce_access':'category',
                            'domain_socio_demographic':'category',
                            'domain_nonsupermarket_proximity':'category',
                            'domain_food_for_families':'category',
                            'domain_fuel_poverty':'category', 
                            'combined': 'category'}
    )
    colormap = ['#0d0887',
                '#41049d',
                '#6a00a8',
                '#8f0da4',
                '#b12a90',
                '#cc4778',
                '#e16462',
                '#f2844b',
                '#fca636',
                '#fcce25']
    colormap.reverse()

    fig = px.scatter_mapbox(
                        df, 
                        lat='latitude',
                        lon='longitude', 
                        color=domain, 
                        color_discrete_sequence=colormap,
                        custom_data=['geo_code', 
                                     'domain_supermarket_proximity',
                                     'domain_supermarket_transport',
                                     'domain_ecommerce_access',
                                     'domain_socio_demographic',
                                     'domain_nonsupermarket_proximity',
                                     'domain_food_for_families',
                                     'domain_fuel_poverty',
                                     'combined'],
                        center={'lat': 53.8067, 'lon': -1.5550}, 
                        category_orders={domain: ['1', '2', '3', '4', '5', '6', '7','8', '9', '10']})
    fig.update_layout(mapbox_style='carto-positron')
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.95,
        xanchor="right",
        x=0.99, 
        itemsizing='constant'
    ))
    fig.update_layout(legend_title_text='Decile (1 = highest priority)')
    
    fig.update_traces(hovertemplate=(
                        '<b>Geo Code</b>: %{customdata[0]}<br>'+\
                        'Proximity to supermarket food retail facilities decile: %{customdata[1]}<br>'+\
                        'Accessibility to supermarket retail facilties decile: %{customdata[2]}<br>'+\
                        'Access to online deliveries decile: %{customdata[3]}<br>'+\
                        'Socio-demographic barriers decile: %{customdata[4]}<br>'+\
                        'Proximity to non-supermarket food retail facilities decile: %{customdata[5]}<br>'+\
                        'Food support for families decile: %{customdata[6]}<br>'+\
                        'Fuel poverty decile: %{customdata[7]}<br>'
                        'Combined Priority Places Index decile: %{customdata[8]}<br>'))
    fig.update_geos(fitbounds="locations", visible=True)
    return fig

if __name__=="__main__":
    app.run(debug=True)