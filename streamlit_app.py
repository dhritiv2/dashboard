import streamlit as st
import pandas as pd
import numpy as np

# Layout configuration
st.set_page_config(layout="wide")


# Header
st.title("Fire Suppression Dashboard")

# Sidebar sections for drone, fire, and base information
with st.sidebar:
    st.subheader("Drone Information")
    drone_tab = st.selectbox("Select Drone", ["Drone 1", "Drone 2", "Drone 3", "Drone 4"])
    st.write("Battery Life: XX%")
    st.write("Drone Speed: XX m/s")
    st.write("Drone Coords: (XX, YY)")
    st.write("Suppressant: XX%")
    st.write("Active: Moving / Idle")
    st.write("Suppressing: Yes / No")

    st.subheader("Fire Information")
    fire_tab = st.selectbox("Select Fire", ["Fire 1", "Fire 2", "Fire 3", "Fire 4"])
    st.write("Fire Coordinates: (AB°, CD°)")
    st.write("Fire Type: Wildfire / Chemical / Electrical / Metal")
    st.write("Size of fire: XX m²")
    st.write("Fire Temperature: XX° C")
    st.write("Fire Growth: XX m²/s")
    st.write("Wind Conditions: 0-15 mph / 15-30 mph / 30-45 mph")

    st.subheader("Base Information")
    base_tab = st.selectbox("Select Base", ["Base 1", "Base 2", "Base 3", "Base 4"])
    st.write("Suppressant Tank: XX% full")
    st.write("Water Tank: XX% full")
    st.write("Coords: (AB°, CD°)")
    st.write("Charging: On / Off")
    st.write("Water: Full / Refill")
    st.write("Suppressant: Full / Refill")

    st.button("Terminate Selected")
    st.button("Terminate All")

# Center map display for drones and fires
st.subheader("Map Display")

# Sample data for displaying map points
drones = pd.DataFrame({
    'lat': [37.76, 37.77, 37.78, 37.79],
    'lon': [-122.43, -122.44, -122.45, -122.46]
})
fires = pd.DataFrame({
    'lat': [37.76, 37.77, 37.78, 37.79],
    'lon': [-122.41, -122.42, -122.43, -122.44]
})

# Display drones and fires on the map
st.map(drones)
st.map(fires)

# Tabs for different views
st.subheader("Views")
view_tab = st.selectbox("Select View", ["Station + Drone + Fire", "Topographical", "Wind", "Heat"])

st.write("Selected View: ", view_tab)
