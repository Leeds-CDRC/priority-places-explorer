from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import json

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Priority Places"
server = app.server

app.layout = html.Div(style={
                        'height': '100vh', 
                        'padding': 10, 
                      }, 
                      children=[
    
    html.H4('CDRC Priority Places'),
    #html.P("Select a domain:"),
    dcc.Dropdown(
        id='domain', 
        options=[{"label": "Priority Places Index", "value": "combined"},
                 {"label": "Proximity to supermarket retail facilities", "value": "domain_supermarket_proximity"}, 
                 {"label": "Accessibility to supermarket retail facilties", "value": "domain_supermarket_transport"}, 
                 {"label": "Access to online deliveries", "value": "domain_ecommerce_access"}, 
                 {"label": "Proximity to non-supermarket food provision", "value": "domain_nonsupermarket_proximity"},
                 {"label": "Socio-demographic barriers", "value": "domain_socio_demographic"}, 
                 {"label": "Food support for families", "value": "domain_food_for_families"}, 
                 {"label": "Fuel poverty", "value": "domain_fuel_poverty"}],
        value='combined',
        multi=False,
        #style={'width': "100%"}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(), 

    dcc.Graph(id="graph", figure={}), 

    html.Div(id='description', children=[

        html.Div(id='col1', children=[
            html.H5('How to use'), 
            html.P("""The CDRC Priority Places Index is a composite index formed of data compiled across seven different dimensions relating to food insecurity for England, Scotland, and Wales. 
                      Its goal is to identify neighbourhoods that are most vulnerable to increases in the cost of living and which have a lack of accessibility to cheap, healthy, and sustainable sources of food."""),
            html.P("""It is developed at the geographic level of Lower Super Output Areas in England and Wales and Data Zones in Scotland (2011 boundaries). Each point on the map corresponds to a geographic area. 
                      Any points coinciding with geographical features such as buildings or residences are reflective of the neighbourhood in which those buildings are a part of and not the building or residence itself."""),
            html.P("""
                      The map displays deciles of the composite index so that each color represents a different 10% increment of the ranked neighbourhoods. That is, those neighbourhoods marked with decile 1 are in the top 10% of Priority Places according to the index. 
                      The map defaults to the composite Priority Places Index but each domain used to form the index can be explored via the drop down menu. Hovering over a point also provides the decile scores for each domain. 
                      The data can be filtered by double-clicking on each legend point. For example, the highest priority neighbourhoods can be viewed by double-clicking the icon for the 1st decile in the legend.
                  """),
            html.H5('Domain Definitions'), 
            html.H6("Proximity to supermarket retail facilities (12.5% of composite index)"),
                html.Li("Average distance to nearest large grocery store (Geolytix Retail Points v15)"),
                html.Li("Average count of stores within 1km (Geolytix Retail Points v15)"),
                html.Br(), 
            html.H6("Accessibility to supermarket retail facilities (12.5% of composite index)"),
                html.Li("Average travel distance (based on a custom built spatial interaction model)"), 
                html.Li("Accessibility via public transport (UK Govt Journey Time Statistics 2017 - 2020)"), 
                html.Br(), 
                  ], style={'padding': 10, 'flex': 1}),
        
        html.Div(id='col2', children=[
            html.H6("Access to online deliveries (12.5% of composite index)"),
                html.Li(["Online groceries availability (", html.A("Newing et. al, 2020", href="https://www.tandfonline.com/doi/full/10.1080/09593969.2021.2017321"), ")"]), 
                html.Li(["Propensity to shop online (", html.A("CDRC Internet User Classification 2018", href="https://data.cdrc.ac.uk/dataset/internet-user-classification"), ")"]), 
                html.Br(),
            html.H6("Proximity to non-supermarket food provision (12.5% of composite index)"), 
                html.Li("Distance to nearest non-supermarket retail food store (Food Standards Agency, accessed 2022-08-23)"), 
                html.Li("Count of non-supermarket retail food stores within 1km (Food Standards Agency, accessed 2022-08-23)"), 
                html.Li(["Average distance to nearest market (", html.A("CDRC data from National Market Traders Federation 2016-2019", href="https://data.cdrc.ac.uk/dataset/national-market-traders-federation"), ")"]), 
                html.Li(["Average count of markets within 1km (", html.A("CDRC data from National Market Traders Federation 2016-2019", href="https://data.cdrc.ac.uk/dataset/national-market-traders-federation"), ")"]), 
                html.Br(),
            html.H6("Socio-economic barriers (16.7% of composite index)"),
                html.Li("Proportion of population experiencing income deprivation (UK Govt Index of Multiple Deprivation 2019-2020)"), 
                html.Li("Proportion of population with no car access (UK Census 2011)"), 
                html.Li("Proportion of population who are pensioners (UK Census 2011)"), 
                html.Br(),
            html.H6("Food support for families (16.7% of composite index)"),
                html.Li("Free school meal eligibility"),
                html.Li("Healthy start voucher usage (England and Wales only)"),
                html.Li(["Distance to nearest food bank (", html.A("Give Food", href="https://www.givefood.org.uk/"), ", accessed 2022-08-19)"]),
                html.Li(["Count of food banks within 1km (", html.A("Give Food", href="https://www.givefood.org.uk/"), ", accessed 2022-08-19)"]),
                html.Br(),
            html.H6("Fuel Poverty (16.7% of composite index)"), 
                html.Li("Proportion of households in fuel poverty (2017 - 2020)"), 
                html.Li("Prepayment meter prevalence, 2017")
            ], style={'padding': 10, 'flex': 1})
        ], style={'display': 'flex', 'flex-direction': 'row'}), 

    dcc.Markdown('''\nPriority Places is developed by the ESRC-funded [Consumer Data Research Centre](https://cdrc.ac.uk/) at the University of Leeds\n''', style={'text-align': 'center'}),
    
                      ])
        

@app.callback(
    Output("graph", "figure"), 
    Input("domain", "value"))
def display_choropleth(domain):
    df = pd.read_csv('/data/priority_places_v0_4_decile_domains_WGS.csv',
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
                        'Priority Places Index decile: %{customdata[8]}<br>'+\
                        'Proximity to supermarket retail facilities decile: %{customdata[1]}<br>'+\
                        'Accessibility to supermarket retail facilties decile: %{customdata[2]}<br>'+\
                        'Access to online deliveries decile: %{customdata[3]}<br>'+\
                        'Socio-demographic barriers decile: %{customdata[4]}<br>'+\
                        'Proximity to non-supermarket food provision decile: %{customdata[5]}<br>'+\
                        'Food support for families decile: %{customdata[6]}<br>'+\
                        'Fuel poverty decile: %{customdata[7]}<br>'))
    fig.update_geos(fitbounds="locations", visible=True)
    return fig

if __name__=="__main__":
    app.run(debug=True)