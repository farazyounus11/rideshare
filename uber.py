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

all_widgets = sp.create_widgets(df, create_data)

res = sp.filter_df(df, all_widgets)
st.title("Streamlit AutoPandas")
st.header("Original DataFrame")
st.write(df)

st.header("Result DataFrame")
st.write(res)
