import streamlit as st
import pandas as pd
import pydeck as pdk
import os

st.title("NYC RideShare Visualization")
st.header('By Faraz Younus | M.S. Stats & Data Science', divider='gray')
st.header('Select month for Visualization!')

files = os.listdir('.')
csv_files = [file for file in files if file.endswith('.csv')]

if not csv_files:
    st.write("No CSV files found in the current directory.")
else:
    selected_file = st.selectbox('Select A Month', csv_files)
    
    if st.button('Select'):
        st.session_state['selected_file'] = selected_file  
if 'selected_file' in st.session_state:
    # Reading the selected CSV file from session state
    df = pd.read_csv(st.session_state['selected_file'])
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])

    # Assuming 'Base' is a column in your DataFrame
    # Get unique bases and allow the user to select
    base_options = df['Base'].unique().tolist()
    selected_bases = st.multiselect('Choose Car Type', base_options, default=base_options)

    if selected_bases:  # Check if any base is selected
        df = df[df['Base'].isin(selected_bases)]

    hour_range = st.slider(
        "Select Hour of Day",
        0, 24, (0, 24),
        step=1,  # Hour steps
        format="%d hours"  # Display format
    )

    # Further filtering DataFrame based on selected hour range
    df['Hour'] = df['Date/Time'].dt.hour
    df = df[df['Hour'].between(hour_range[0], hour_range[1], inclusive='both')]
    base_count = df['Base'].value_counts(normalize=True) * 100  # normalize=True gives the relative frequencies
    percentagedf = pd.DataFrame(base_count).reset_index()
    percentagedf.columns = ['Base', 'Percentage']
    col1, col2 = st.columns(2)

    with col1:
        st.write("This is the Data!")
        st.write(df)

    with col2:
        st.write("Percentage Distribution of Ride Type")
        st.write(percentagedf)


    st.header('Map', divider='gray')
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=["Lon", "Lat"],
        get_color=[255, 255, 0],  # Yellow color for visibility
        get_radius=12,
    )
    
    # Define the PyDeck view state for initial map focus
    view_state = pdk.ViewState(latitude=df['Lat'].mean(), longitude=df['Lon'].mean(), zoom=10)
    
    # Create the PyDeck chart
    map = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
    )
    
    # Display the map in Streamlit
    st.pydeck_chart(map)
