from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import os

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/jpg;base64,{}'.format(encoded.decode())



df = pd.read_csv('/app/data/priority_places_Oct2022_WGS.csv',
                    dtype={'pp_dec_domain_supermarket_proximity':'category',
                        'pp_dec_domain_supermarket_accessibility':'category',
                        'pp_dec_domain_ecommerce_access':'category',
                        'pp_dec_domain_socio_demographic':'category',
                        'pp_dec_domain_nonsupermarket_proximity':'category',
                        'pp_dec_domain_food_for_families':'category',
                        'pp_dec_domain_fuel_poverty':'category', 
                        'pp_dec_combined': 'category'}
)


df['label_domain_supermarket_transport'] = df.loc[:, 'pp_dec_domain_supermarket_accessibility'].replace('0', 'NA')
df['label_domain_ecommerce_access'] = df.loc[:, 'pp_dec_domain_ecommerce_access'].replace('0', 'NA')
df['label_domain_fuel_poverty'] = df.loc[:, 'pp_dec_domain_fuel_poverty'].replace('0', 'NA')


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

# Add google analytics tag if the website hostname environment variable matches
if os.getenv('WEBSITE_HOSTNAME')=='priority-places-explorer.azurewebsites.net':
    with open('ga.html','r') as f:
        app.index_string = f.read()


app.layout = html.Div(
    style={'height': '100vh', 
           'padding': 10,
           'overflow': 'scroll'}, 
    children=[
        ### Top banner
        dbc.Row([
            dbc.Col(
                html.A(
                    html.Img(
                        src=encode_image('assets/CDRC-logo.png'), 
                        height=75,
                    ), 
                    href="https://www.cdrc.ac.uk/",
                )
            ),
            dbc.Col(
                html.H2(
                    'Priority Places for Food Index', 
                    style={'color':'#292929'}, 
                ), 
                align='center'
            ),
            dbc.Col(
                html.Div(
                    html.A(
                        html.Img(
                            src=encode_image('assets/Which-logo-small.png'), 
                            height=75
                        ), 
                        href="https://www.which.co.uk/"
                    ),
                    style={"float": "right"}, 
                ),
            )
        ]),
        html.Br(),
        html.Div(
            # Options for map visualisation
            id='output_container', 
            children=[
                dcc.Dropdown(
                    id='domain', 
                    options=[
                        {"label": "Priority Places for Food Index", "value": "pp_dec_combined"},
                        {"label": "Proximity to supermarket retail facilities", "value": "pp_dec_domain_supermarket_proximity"}, 
                        {"label": "Accessibility to supermarket retail facilties", "value": "pp_dec_domain_supermarket_accessibility"}, 
                        {"label": "Access to online deliveries", "value": "pp_dec_domain_ecommerce_access"}, 
                        {"label": "Proximity to non-supermarket food provision", "value": "pp_dec_domain_nonsupermarket_proximity"},
                        {"label": "Socio-demographic barriers", "value": "pp_dec_domain_socio_demographic"}, 
                        {"label": "Need for family food support", "value": "pp_dec_domain_food_for_families"}, 
                        {"label": "Fuel poverty", "value": "pp_dec_domain_fuel_poverty"}
                    ],
                    value='pp_dec_combined',
                    multi=False,
                ),
                dbc.Row([
                    dbc.Col(
                        html.Div(
                            html.Small("Show supermarket locations:"), 
                            style={'float':'right'}
                        ), 
                        width=True
                    ),
                    dbc.Col(
                        html.Div(
                            daq.BooleanSwitch(
                                id='retailer_switch',
                                on=False,
                                labelPosition='top',
                            ),
                            style={'float': 'right'},
                        ),
                        width='auto'
                    )
                ])
            ]
        ),
        html.Br(), 
        dcc.Loading(
            # The visualisation
            id="loading-1",
            type="default",
            children=dcc.Graph(
                id="graph", 
                figure={}
            ), 
        ),
        html.Div(
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.P("""The Priority Places for Food Index is a composite index formed of data compiled across seven different dimensions relating to food insecurity for England, Scotland, Wales, and Northern Ireland. 
                                      Its goal is to identify neighbourhoods that are most vulnerable to increases in the cost of living and which have a lack of accessibility to cheap, healthy, and sustainable sources of food."""),
                            html.P("""It is developed at the geographic level of Lower Super Output Areas in England and Wales, Data Zones in Scotland and Super Output Areas in Northern Ireland (2011 boundaries). 
                                      Data for all countries is included where possible, but some indicators are not available across all countries. The list of indicators in the domain definitions section below lists the country availability (E=England, S=Scotland, W=Wales, NI=Northern Ireland)."""),
                            html.P(
                                    [
                                        """Technical documentation for the index construction is available via the """, 
                                        html.A(
                                            "CDRC Data Portal", 
                                            href="https://data.cdrc.ac.uk/dataset/priority-places-food-index"
                                        ), 
                                        "."
                                    ]
                                )
                            ], 
                        title='What is the Priority Places for Food Index?'
                    ),
                    dbc.AccordionItem(
                        [
                            html.P("""Each point on the map corresponds to a geographic area. Any points coinciding with geographical features such as buildings or residences are reflective of the neighbourhood in which those buildings are a part of and not the building or residence itself."""),
                            html.P("""The map displays deciles of the composite index so that each color represents a different 10% increment of the ranked neighbourhoods. Those neighbourhoods marked with decile 1 are in the top 10% of Priority Places according to the index."""),
                            html.P("""The map initially displays only the top 10% of places according to the composite Priority Places Index. Each domain used to form the index can be explored via the drop down menu. The other deciles can also be added to the map by clicking the coloured points on the legend."""),
                            html.P("""Hovering over a point also provides the decile scores for each domain."""),
                            html.P(
                                [
                                    """Supermarket and convenience store locations can be added to the map via the toggle switch. These locations are obtained from """, 
                                    html.A(
                                        "Geolytix Retail Points v24", 
                                        href="https://geolytix.com/blog/supermarket-retail-points/"
                                    ), 
                                    "."
                                ]
                            )
                        ], 
                    title='How to use the map',
                    ), 
                    dbc.AccordionItem(
                        [
                            html.H6("Proximity to supermarket retail facilities (12.5% of composite index)"),
                            html.Li([
                                "Average distance to nearest large grocery store (",
                                html.A(
                                    "Geolytix Retail Points v15",
                                    href="https://geolytix.com/blog/supermarket-retail-points/",
                                ),
                                "). E,S,W,NI"
                            ]),
                            html.Br(),
                            html.Li([
                                "Average count of stores within 1km (",
                                html.A(
                                    "Geolytix Retail Points v15",
                                    href="https://geolytix.com/blog/supermarket-retail-points/",
                                ),
                                "). E,S,W,NI"
                            ]),
                            html.Br(),
                            html.H6("Accessibility to supermarket retail facilities (12.5% of composite index)"),
                            html.Li("Average travel distance (based on a custom built spatial interaction model). E,S,W"), 
                            html.Li("Accessibility via public transport (Govt Journey Time Statistics 2017 - 2020). E,S,W"), 
                            html.Br(), 
                            html.H6("Access to online deliveries (12.5% of composite index)"),
                            html.Li([
                                "Online groceries availability (", 
                                html.A(
                                    "Newing et. al, 2020", 
                                    href="https://www.tandfonline.com/doi/full/10.1080/09593969.2021.2017321"
                                ), 
                                ",). E,S,W"
                            ]), 
                            html.Li([
                                "Propensity to shop online (", 
                                html.A(
                                    "CDRC Internet User Classification 2018", 
                                    href="https://data.cdrc.ac.uk/dataset/internet-user-classification"
                                ), 
                                "). E,S,W"
                            ]), 
                            html.Br(),
                            html.H6("Proximity to non-supermarket food provision (12.5% of composite index)"), 
                            html.Li("Distance to nearest non-supermarket retail food store (Food Standards Agency, accessed 2022-08-23). E,S,W,NI"), 
                            html.Li("Count of non-supermarket retail food stores within 1km (Food Standards Agency, accessed 2022-08-23). E,S,W,NI"), 
                            html.Li([
                                "Average distance to nearest market (", 
                                html.A(
                                    "CDRC data from National Market Traders Federation 2016-2019", 
                                    href="https://data.cdrc.ac.uk/dataset/national-market-traders-federation"
                                ), 
                                "). E,W."
                            ]), 
                            html.Li([
                                "Average count of markets within 1km (", 
                                html.A(
                                    "CDRC data from National Market Traders Federation 2016-2019", 
                                    href="https://data.cdrc.ac.uk/dataset/national-market-traders-federation"
                                ), 
                                "). E,W"
                            ]), 
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
                        ], 
                        title='Domain definitions'
                    )
                ]
            )
        ), 
        html.Br(),
        dcc.Markdown('''\nPriority Places is developed by the ESRC-funded [Consumer Data Research Centre](https://cdrc.ac.uk/) at the University of Leeds in collaboration with [Which?](https://which.co.uk)\n''', style={'text-align': 'center'}),
        html.Div([
                html.A(
                    html.Small('Privacy and Cookies'), 
                    href="https://www.cdrc.ac.uk/privacy/"
                )
            ], 
            style={'textAlign': 'center'}
        ),
    ]
)

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
                        custom_data=['geo_label', 
                                     'pp_dec_domain_supermarket_proximity',
                                     'label_domain_supermarket_transport',
                                     'label_domain_ecommerce_access',
                                     'pp_dec_domain_socio_demographic',
                                     'pp_dec_domain_nonsupermarket_proximity',
                                     'pp_dec_domain_food_for_families',
                                     'label_domain_fuel_poverty',
                                     'pp_dec_combined', 
                                     'geo_code'],
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
                        str('<b>%{customdata[0]} (%{customdata[9]})</b><br>')+\
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
                        selector=-1)

        fig.data[-1]['marker'] = {'color': '#808080', 'opacity':0.2}
        fig.update_layout(coloraxis_showscale=False)

    fig.update_geos(fitbounds="locations", visible=True)
    return fig

if __name__=="__main__":
    app.run()
