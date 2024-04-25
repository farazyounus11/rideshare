import streamlit as st
import pandas as pd
import streamlit_pandas as sp
import pydeck as pdk
import os

@st.cache
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date/Time']).dt.date
    df['Hour'] = pd.to_datetime(df['Date/Time']).dt.hour
    df.drop(columns=['Date/Time'], inplace=True)
    return df

file_options = ["April.csv", "August.csv", "July.csv", "June.csv","May.csv","September.csv"]
selected_file = st.selectbox("Select a file", file_options)
df = load_data(selected_file)
create_data = {"Date": "select",
                "Hour": "multiselect",
              "Base": "select"}

all_widgets = sp.create_widgets(df, create_data, ignore_columns=[["lat","lon"]])

res = sp.filter_df(df, all_widgets)
st.title("Streamlit AutoPandas")
st.header("Original DataFrame")
st.write(df)

st.header("Result DataFrame")
st.write(res)

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=40.7128,  # NYC latitude
        longitude=-74.0060,  # NYC longitude
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=res,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=res,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))
