import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# add title for this image
st.header("Distributed Car Detection System")
st.image("./cars/car_1221.jpg", caption="Target Car", use_column_width=True) 

conn = sqlite3.connect("./db/synthetic.db")
df = pd.read_sql_query("SELECT * FROM mqtt_data", conn)

df['timestamp'] = pd.to_datetime(df['timestamp'])

fig = px.line(df, x='timestamp', y='location', color='location', title='Car Detection Timeline')

fig.update_traces(mode='markers+lines')  
fig.update_layout(yaxis_title='') 


fig2 = px.histogram(df, x='location', title='Camera Activity')

location_coords = {
    "Location-1": {"lat": 10.047470, "lon": 76.318569},  
    "Location-2": {"lat": 10.042392, "lon": 76.328312}   
}

location_colors = {
    "Location-1": '#0000ff',  
    "Location-2": '#FF0000',   
}

df['latitude'] = df['location'].map(lambda x: location_coords[x]['lat'])
df['longitude'] = df['location'].map(lambda x: location_coords[x]['lon'])
df['color'] = df['location'].map(lambda x: location_colors[x])

st.map(df, latitude='latitude', longitude='longitude', color='color', zoom=13)

st.plotly_chart(fig)
st.plotly_chart(fig2)
