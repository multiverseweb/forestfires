import streamlit as st
import pandas as pd
import datetime
import pydeck as pdk

st.title("Forest Fires worldwide 🌳🔥")

@st.cache(persist = True)
def importing_dataset ():
    # Passing the file to pandas dataframe and formating the values types
    df_focos = pd.read_csv('data/ForestFires.csv', encoding='utf-8')

    df_focos[['satelite']] = df_focos[['satelite']].astype('category')
    df_focos[['pais']] = df_focos[['pais']].astype('category')
    df_focos[['data_hora_gmt']] = df_focos[['data_hora_gmt']].astype('category')

    floats = df_focos.select_dtypes(include=['float64']).columns.tolist()
    df_focos[floats] = df_focos[floats].astype('float32')

    df_focos['data_hora_gmt'] = pd.to_datetime(df_focos['data_hora_gmt'])

    return df_focos

def choosing_variables():
    # Date selection
    date = st.date_input("Choose a July 2022 date",datetime.date(2022, 8, 6))
    
    # Country selection
    all_options_country = df_focos['pais'].unique()
    select_country = st.multiselect("Country options (Leave blank to allow all countries)", all_options_country, ['Brasil'])

    if len(select_country) > 0:
        temp_select_country = select_country
    else:
        temp_select_country = all_options_country

    # Satellite selection
    all_options_satellite = df_focos['satelite'].unique()
    select_satellite = st.multiselect("satellite options (Leave blank to allow all satellites)", all_options_satellite, ['NOAA-20'])

    if len(select_satellite) > 0:
        temp_select_satellite = select_satellite
    else:
        temp_select_satellite = all_options_satellite

    return date, temp_select_country, temp_select_satellite

df_focos = importing_dataset()

# Defining initial date country and satellite variables
date = datetime.datetime.strptime('19082022', "%d%m%Y").date()
temp_select_country = ['Brasil']
temp_select_satellite = ['NOAA-20']

# Hidding the possible options
if st.checkbox("Show options", True):
    date, temp_select_country, temp_select_satellite = choosing_variables()

# Querying the df_focos dataframe
df_focos = df_focos[(df_focos['data_hora_gmt'].dt.date == date) & 
                    (df_focos['pais'].isin(temp_select_country)) &
                    (df_focos['satelite'].isin(temp_select_satellite))]

# Defining the Latitude and Longite as 0 to centre the map
lat0=0
lon0=0

# Define a layer to display on a map
layer = pdk.Layer(
    "ColumnLayer",
    df_focos,
    get_position='[lon, lat]',
    elevation_scale=50,
    pickable=True,
    elevation_range=[50, 500],
    get_fill_color=[180, 0, 200, 140],
    extruded=True,
    radius=25,
    coverage=50,
    auto_highlight=True,
)

# Set the viewport location
view_state = pdk.ViewState(latitude=lat0, longitude=lon0, zoom=0.5, bearing=0, pitch=45)

# Generating tooltip for each generated point in the map with the related satellite
tooltip = {
    "html": "satellite: <b>{satellite}</b>",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}

# Rendering the map 
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/dark-v10',
    tooltip=tooltip
))