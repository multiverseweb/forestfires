import numpy as np
import streamlit as st
import pandas as pd
import urllib
import datetime
import pydeck as pdk
from pydeck.types import String



#running streamlit -> streamlit run app.py

st.title("Forest Fires")

@st.cache(persist = True)
def importing_dataset ():
    df_focos = pd.read_csv('data/ForestFires.csv', encoding='utf-8')
    df_focos[['satelite']] = df_focos[['satelite']].astype('category')
    df_focos[['risco_fogo']] = df_focos[['risco_fogo']].astype('category')
    df_focos[['pais']] = df_focos[['pais']].astype('category')
    df_focos[['data_hora_gmt']] = df_focos[['data_hora_gmt']].astype('category')

    floats = df_focos.select_dtypes(include=['float64']).columns.tolist()
    df_focos[floats] = df_focos[floats].astype('float32')
    df_focos['data_hora_gmt'] = pd.to_datetime(df_focos['data_hora_gmt'])

    df_focos['risco_fogo'] = df_focos['risco_fogo'].fillna(0)

    return df_focos

df_focos = importing_dataset()


date = datetime.datetime.strptime('06082022', "%d%m%Y").date()
temp_select_country = ['Brasil']
temp_select_satelite = ['NOAA-20']

if st.checkbox("Show options", True):
    # Date selection
    date = st.date_input("Day to look at",datetime.date(2022, 8, 6))
    
    # Country selection
    all_options_country = df_focos['pais'].unique()

    select_country = st.multiselect("Country options (Leave blank to allow all countries)", all_options_country, ['Brasil'] )

    if len(select_country) > 0:
        temp_select_country = select_country
    else:
        temp_select_country = all_options_country

    # Satelite selection
    all_options_satelite = df_focos['satelite'].unique()

    select_satelite = st.multiselect("Satelite options (Leave blank to allow all satelites)", all_options_satelite, ['NOAA-20'] )

    if len(select_satelite) > 0:
        temp_select_satelite = select_satelite
    else:
        temp_select_satelite = all_options_satelite


# Query
df_focos = df_focos[(df_focos['data_hora_gmt'].dt.date == date) & 
                    (df_focos['pais'].isin(temp_select_country)) &
                    (df_focos['satelite'].isin(temp_select_satelite))]


focos = df_focos[['lat', 'lon', 'satelite']].reset_index()

lat0=0
lon0=0

# Define a layer to display on a map
layer = pdk.Layer(
    'HexagonLayer',
    focos,
    get_position='[lon, lat]',
    elevation_scale=1000,
    pickable=True,
    elevation_range=[100, 500],
    colorRange=[255,0,0],
    extruded=True,
    radius=25,
    coverage=300,
)

# Set the viewport location
view_state = pdk.ViewState(latitude=lat0, longitude=lon0, zoom=0.5, bearing=0, pitch=45)

# Render
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/dark-v10',
))