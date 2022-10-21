from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import base64

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/jpg;base64,{}'.format(encoded.decode())

df = pd.read_csv('/app/data/priority_places_v1_2_decile_domains_WGS.csv',
                    dtype={'domain_supermarket_proximity':'category',
                        'domain_supermarket_transport':'category',
                        'domain_ecommerce_access':'category',
                        'domain_socio_demographic':'category',
                        'domain_nonsupermarket_proximity':'category',
                        'domain_food_for_families':'category',
                        'domain_fuel_poverty':'category', 
                        'combined': 'category'}
)


df['label_domain_supermarket_transport'] = df.loc[:, 'domain_supermarket_transport'].replace('-1', 'NA')
df['label_domain_ecommerce_access'] = df.loc[:, 'domain_ecommerce_access'].replace('-1', 'NA')
df['label_domain_fuel_poverty'] = df.loc[:, 'domain_fuel_poverty'].replace('-1', 'NA')

retailers = pd.read_csv('/app/data/retail_locations_glxv24_202206.csv')

colormap = ['#0d0887',
            '#41049d',
            '#6a00a8',
            '#8f0da4',
            '#b12a90',
            '#c94a79',
            '#db6a68',
            '#e58858',
            '#e8a34a',
            '#e1bf40']
        

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Priority Places"
server = app.server


########################################################################
#
#  For Google Analytics
#
########################################################################
# app.index_string = """<!DOCTYPE html>
# <html>
#     <head>
#         <!-- Google tag (gtag.js) -->
#         <script async src="https://www.googletagmanager.com/gtag/js?id=UA-246336486-1"></script>
#         <script>
#         window.dataLayer = window.dataLayer || [];
#         function gtag(){dataLayer.push(arguments);}
#         gtag('js', new Date());

#         gtag('config', 'UA-246336486-1');
#         </script>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>"""

#pil_image = Image.open("assets/CDRC-logo.jpg")


app.layout = html.Div(style={
                    'height': '100vh', 
                    'padding': 10, 
                    }, 
                    children=[

html.A(html.Img(src=encode_image('assets/CDRC-logo.png'), height=75), href="https://www.cdrc.ac.uk/"),
html.Br(),
html.Br(),
html.H4('Priority Places for Food'),

html.Div(id='output_container', children=[
    dcc.Dropdown(
        id='domain', 
        options=[{"label": "Priority Places Index", "value": "combined"},
                {"label": "Proximity to supermarket retail facilities", "value": "domain_supermarket_proximity"}, 
                {"label": "Accessibility to supermarket retail facilties", "value": "domain_supermarket_transport"}, 
                {"label": "Access to online deliveries", "value": "domain_ecommerce_access"}, 
                {"label": "Proximity to non-supermarket food provision", "value": "domain_nonsupermarket_proximity"},
                {"label": "Socio-demographic barriers", "value": "domain_socio_demographic"}, 
                {"label": "Need for family food support", "value": "domain_food_for_families"}, 
                {"label": "Fuel poverty", "value": "domain_fuel_poverty"}],
        value='combined',
        multi=False,
        #style={'width': "100%"}
    ),
    daq.BooleanSwitch(
        id='retailer_switch',
        on=False,
        label='Show supermarket locations',
        labelPosition='top'
    )
]),
html.Br(), 
dcc.Loading(
        id="loading-1",
        type="default",
        children=dcc.Graph(id="graph", figure={}), 
    ),
html.Div(id='description', children=[
    html.Div(id='col1', children=[
        html.H5('How to use'), 
        html.P("""The CDRC Priority Places Index is a composite index formed of data compiled across seven different dimensions relating to food insecurity for England, Scotland, Wales, and Northern Ireland. 
                    Its goal is to identify neighbourhoods that are most vulnerable to increases in the cost of living and which have a lack of accessibility to cheap, healthy, and sustainable sources of food."""),
        html.P("""It is developed at the geographic level of Lower Super Output Areas in England and Wales, Data Zones in Scotland and Super Output Areas in Northern Ireland (2011 boundaries). Each point on the map corresponds to a geographic area. 
                    Any points coinciding with geographical features such as buildings or residences are reflective of the neighbourhood in which those buildings are a part of and not the building or residence itself."""),
        html.P("""
                    The map displays deciles of the composite index so that each color represents a different 10% increment of the ranked neighbourhoods. That is, those neighbourhoods marked with decile 1 are in the top 10% of Priority Places according to the index.
                    The map initially displays only the top 10% of places according to the composite Priority Places Index. Each domain used to form the index can be explored via the drop down menu. The other deciles can also be added to the map by clicking the coloured points on the legend.
                    Hovering over a point also provides the decile scores for each domain. 
                """),
        html.P("""Data for all countries is included where possible, but some indicators are not available across all countries. The list of indiciators below lists the country availability."""),
        html.P(["""Supermarket and convenience store locations can be added to the map via the toggle switch. These locations are obtained from """, html.A("Geolytix Retail Points v24", href="https://geolytix.com/blog/supermarket-retail-points/"), "."]),
        html.H5('Domain Definitions'), 
        html.H6("Proximity to supermarket retail facilities (12.5% of composite index)"),
            html.Li("Average distance to nearest large grocery store (Geolytix Retail Points v15). E,S,W,NI"),
            html.Li("Average count of stores within 1km (Geolytix Retail Points v15). E,S,W,NI"),
            html.Br(), 
                ], style={'padding': 10, 'flex': 1}),
    
    html.Div(id='col2', children=[
        html.H6("Accessibility to supermarket retail facilities (12.5% of composite index)"),
            html.Li("Average travel distance (based on a custom built spatial interaction model). E,S,W"), 
            html.Li("Accessibility via public transport (Govt Journey Time Statistics 2017 - 2020). E,S,W"), 
            html.Br(), 
        html.H6("Access to online deliveries (12.5% of composite index)"),
            html.Li(["Online groceries availability (", html.A("Newing et. al, 2020", href="https://www.tandfonline.com/doi/full/10.1080/09593969.2021.2017321"), ",). E,S,W"]), 
            html.Li(["Propensity to shop online (", html.A("CDRC Internet User Classification 2018", href="https://data.cdrc.ac.uk/dataset/internet-user-classification"), "). E,S,W"]), 
            html.Br(),
        html.H6("Proximity to non-supermarket food provision (12.5% of composite index)"), 
            html.Li("Distance to nearest non-supermarket retail food store (Food Standards Agency, accessed 2022-08-23). E,S,W,NI"), 
            html.Li("Count of non-supermarket retail food stores within 1km (Food Standards Agency, accessed 2022-08-23). E,S,W,NI"), 
            html.Li(["Average distance to nearest market (", html.A("CDRC data from National Market Traders Federation 2016-2019", href="https://data.cdrc.ac.uk/dataset/national-market-traders-federation"), "). E,W."]), 
            html.Li(["Average count of markets within 1km (", html.A("CDRC data from National Market Traders Federation 2016-2019", href="https://data.cdrc.ac.uk/dataset/national-market-traders-federation"), "). E,W"]), 
            html.Br(),
        html.H6("Socio-demographic barriers (16.7% of composite index)"),
            html.Li("Proportion of population experiencing income deprivation (UK Govt Index of Multiple Deprivation 2017-2020). E,S,W,NI"), 
            html.Li("Proportion of population with no car access (UK Census 2011). E,S,W,NI"), 
            html.Br(),
        html.H6("Need for family food support (16.7% of composite index)"),
            html.Li("Free school meal eligibility. E,S,W,NI"),
            html.Li("Healthy start voucher usage (England and Wales only). E,W."),
            html.Li(["Distance to nearest food bank (", html.A("Give Food", href="https://www.givefood.org.uk/"), ", accessed 2022-08-19). E,S,W,NI"]),
            html.Br(),
        html.H6("Fuel Poverty (16.7% of composite index)"), 
            html.Li("Proportion of households in fuel poverty (2017 - 2020). E,S,W."), 
            html.Li("Prepayment meter prevalence, 2017. E,S,W")
        ], style={'padding': 10, 'flex': 1})
    ], style={'display': 'flex', 'flex-direction': 'row'}), 

dcc.Markdown('''\nPriority Places is developed by the ESRC-funded [Consumer Data Research Centre](https://cdrc.ac.uk/) at the University of Leeds in collaboration with [Which?](https://which.co.uk)\n''', style={'text-align': 'center'}),
html.Div([
        html.A('Privacy and Cookies', href="https://www.cdrc.ac.uk/privacy/")
], style={'textAlign': 'center'}),
               ])


@app.callback(
Output("graph", "figure"), 
Input("domain", "value"), 
Input("retailer_switch", "on"))
def display_map(domain, show_retailers):

    fig = px.scatter_mapbox(
                        df, 
                        lat='latitude',
                        lon='longitude', 
                        color=domain, 
                        color_discrete_sequence=colormap,
                        custom_data=['geo_code', 
                                        'domain_supermarket_proximity',
                                        'label_domain_supermarket_transport',
                                        'label_domain_ecommerce_access',
                                        'domain_socio_demographic',
                                        'domain_nonsupermarket_proximity',
                                        'domain_food_for_families',
                                        'label_domain_fuel_poverty',
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
                        str('<b>Geo Code</b>: %{customdata[0]}<br>')+\
                        str('Priority Places Index decile: %{customdata[8]}<br>')+\
                        str('Proximity to supermarket retail facilities decile: %{customdata[1]}<br>')+\
                        str('Accessibility to supermarket retail facilties decile: %{customdata[2]}<br>').replace('-1', 'NA')+\
                        str('Access to online deliveries decile: %{customdata[3]}<br>').replace('-1', 'NA')+\
                        str('Proximity to non-supermarket food provision decile: %{customdata[5]}<br>')+\
                        str('Socio-demographic barriers decile: %{customdata[4]}<br>')+\
                        str('Food support for families decile: %{customdata[6]}<br>')+\
                        str('Fuel poverty decile: %{customdata[7]}<br>').replace('-1', 'NA')))
    fig.update_traces(visible='legendonly', selector=(lambda x: int(x.name) > 1))
    fig.update_traces(visible=False, selector=(lambda x: x.name=='-1'))

    if show_retailers:
        
        fig2 = px.scatter_mapbox(retailers, 
                                    lat='lat_wgs', 
                                    lon='long_wgs', 
                                    custom_data=['retailer', 'size_code'],
        )

        fig.add_trace(fig2.data[0])
        fig.update_traces(hovertemplate=(
                                '<b>%{customdata[0]}</b><br>'+\
                                'Size: %{customdata[1]}<br>'), 
                        selector=10)

        fig.data[-1]['marker'] = {'color': '#808080', 'opacity':0.2}
        fig.update_layout(coloraxis_showscale=False)

    fig.update_geos(fitbounds="locations", visible=True)
    return fig

if __name__=="__main__":
    app.run(debug=True)