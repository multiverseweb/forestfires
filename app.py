import streamlit as st
import pandas as pd
import datetime
import pydeck as pdk

st.set_page_config(layout="wide")

st.title("Forest Fire Prediction 🌳🔥")

@st.cache(persist = True)
def importing_dataset ():
    # Passing the file to df_heatSpots dataframe and formating the values types
    df_heatSpots0 = pd.read_csv('data/ForestFires0.csv', encoding='utf-8')
    df_heatSpots1 = pd.read_csv('data/ForestFires1.csv', encoding='utf-8')
    df_heatSpots2 = pd.read_csv('data/ForestFires2.csv', encoding='utf-8')
    frames = [df_heatSpots0, df_heatSpots1, df_heatSpots2]
    df_heatSpots = pd.concat(frames)

    df_heatSpots[['satellite']] = df_heatSpots[['satellite']].astype('category')
    df_heatSpots[['country']] = df_heatSpots[['country']].astype('category')
    df_heatSpots[['date_hour_gmt']] = df_heatSpots[['date_hour_gmt']].astype('category')

    floats = df_heatSpots.select_dtypes(include=['float64']).columns.tolist()
    df_heatSpots[floats] = df_heatSpots[floats].astype('float32')

    df_heatSpots['date_hour_gmt'] = pd.to_datetime(df_heatSpots['date_hour_gmt'])

    return df_heatSpots

def choosing_variables():
    # Date selection
    with st.sidebar:
        st.sidebar.markdown("**First select the data range you want to analyze:** 👇")
        date = st.date_input("Choose an August 2022 date",datetime.date(2022, 8, 6))
    
        # Country selection
        all_options_country = df_heatSpots['country'].unique()
        select_country = st.multiselect("Country", all_options_country, ['India'])

        if len(select_country) > 0:
            temp_select_country = select_country
        else:
            temp_select_country = all_options_country

        # Satellite selection
        all_options_satellite = df_heatSpots['satellite'].unique()
        select_satellite = st.multiselect("Satellite", all_options_satellite, ['NOAA-20'])

        if len(select_satellite) > 0:
            temp_select_satellite = select_satellite
        else:
            temp_select_satellite = all_options_satellite

    return date, temp_select_country, temp_select_satellite


df_heatSpots = importing_dataset()

# Defining initial date country and satellite variables
date = datetime.datetime.strptime('19082022', "%d%m%Y").date()
temp_select_country = ['India']
temp_select_satellite = ['NOAA-20']

# Hidding the possible options
date, temp_select_country, temp_select_satellite = choosing_variables()

# Querying the df_heatSpots dataframe
df_heatSpots = df_heatSpots[(df_heatSpots['date_hour_gmt'].dt.date == date) & 
                    (df_heatSpots['country'].isin(temp_select_country)) &
                    (df_heatSpots['satellite'].isin(temp_select_satellite))]

# Defining the Latitude and Longite as 0 to centre the map
lat0=0
lon0=0

# Set the viewport location
view_state = pdk.ViewState(latitude=lat0, longitude=lon0, zoom=1.9, bearing=0, pitch=45)

# Define a layer to display on a map
layer = pdk.Layer(
    "ColumnLayer",
    df_heatSpots,
    get_position='[lon, lat]',
    elevation_scale=150,
    pickable=True,
    elevation_range=[50, 500],
    get_fill_color=[3, 252, 227, 140],
    extruded=True,
    radius=25,
    coverage=50,
    auto_highlight=True,
)

# Generating tooltip for each generated point in the map with the related satellite
tooltip = {
    "html": "satellite: <b>{satellite}</b>",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}

print(type(tooltip))
print(type(view_state))
print(type(layer))

# Rendering the map 
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/dark-v10',
    tooltip=tooltip,
))

print(" ")
print(type(st.pydeck_chart))


# streamlit run app.py