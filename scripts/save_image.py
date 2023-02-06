import pandas as pd
import plotly.express as px

"""
This script implements the same plotly express map as used in the priority places explorer 
tool but uses the plotly write_image function to save a static image to the desired location.
"""

df = pd.read_csv('data/priority_places_Oct2022_WGS.csv',
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

retailers = pd.read_csv('data/retail_locations_glxv24_202206.csv')

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

domain = 'pp_dec_combined'

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
                    category_orders={domain: ['1', '2', '3', '4', '5', '6', '7','8', '9', '10']}, 
                    zoom=9)
    
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

#fig.update_traces(visible='legendonly', selector=(lambda x: int(x.name) not in [1,5,10]))
fig.update_traces(visible=False, selector=(lambda x: x.name=='-1'))

fig.write_image("output_images/basemap_leeds_bradford.png", format='png', scale=4.0, width=1500, height=800)