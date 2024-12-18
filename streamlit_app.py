import streamlit as st
import random
import folium
from folium import plugins

#simulate different data for drones, fires, and bases only once per session, change later
def get_drone_data():
    return {
        "Battery Life": f"{random.randint(10, 100)}%",
        "Drone Speed": f"{random.uniform(0, 50):.1f} m/s",
        "Coords": (random.uniform(-90, 90), random.uniform(-180, 180)),
        "Suppressant Level": f"{random.randint(0, 100)}%",
        "Active": random.choice(["Moving", "Idle"]),
        "Suppressing": random.choice(["Yes", "No"])
    }

def get_fire_data():
    return {
        "Coords": (random.uniform(-90, 90), random.uniform(-180, 180)),
        "Type": random.choice(["Wildfire", "Chemical", "Electrical", "Metal"]),
        "Size": f"{random.uniform(0, 1000):.1f} m²",
        "Temperature": f"{random.uniform(300, 1500):.1f} °C",
        "Growth Rate": f"{random.uniform(0, 50):.1f} m²/s",
        "Wind Conditions": random.choice(["0-15 mph", "15-30 mph", "30-45 mph"])
    }

def get_base_data():
    return {
        "Suppressant Tank": f"{random.randint(0, 100)}% full",
        "Water Tank": f"{random.randint(0, 100)}% full",
        "Coords": (random.uniform(-90, 90), random.uniform(-180, 180)),
        "Charging": random.choice(["On", "Off"]),
        "Water": random.choice(["Full", "Refill"]),
        "Suppressant": random.choice(["Full", "Refill"])
    }

#initialize session state for drones fire s and bases
if "drone_data" not in st.session_state:
    st.session_state.drone_data = {f"Drone {i}": get_drone_data() for i in range(1, 5)}

if "fire_data" not in st.session_state:
    st.session_state.fire_data = {f"Fire {i}": get_fire_data() for i in range(1, 5)}

if "base_data" not in st.session_state:
    st.session_state.base_data = {f"Base {i}": get_base_data() for i in range(1, 5)}

#sidebar for selections and data display
st.sidebar.header("Select Drone")
drone_options = list(st.session_state.drone_data.keys())
selected_drone = st.sidebar.selectbox("Choose a drone to view data:", drone_options)

st.sidebar.subheader(f"{selected_drone} Data")
for key, value in st.session_state.drone_data[selected_drone].items():
    st.sidebar.write(f"{key}: {value}")

st.sidebar.header("Select Fire")
fire_options = list(st.session_state.fire_data.keys())
selected_fire = st.sidebar.selectbox("Choose a fire to view data:", fire_options)

st.sidebar.subheader(f"{selected_fire} Data")
for key, value in st.session_state.fire_data[selected_fire].items():
    st.sidebar.write(f"{key}: {value}")

st.sidebar.header("Select Base")
base_options = list(st.session_state.base_data.keys())
selected_base = st.sidebar.selectbox("Choose a base to view data:", base_options)

st.sidebar.subheader(f"{selected_base} Data")
for key, value in st.session_state.base_data[selected_base].items():
    st.sidebar.write(f"{key}: {value}")


st.header("Fire Suppression Dashboard")

#map type selection
st.subheader("Maps")
layer_options = ["Station + Drone + Fire", "Topographical", "Wind", "Heat"]
selected_layer = st.selectbox("Choose a layer to display:", layer_options)

#create a folium map based on the selected layer
if selected_layer == "Station + Drone + Fire":
    m = folium.Map(location=[0, 0], zoom_start=2)
    for drone, data in st.session_state.drone_data.items():
        folium.Marker(
            location=data["Coords"],
            popup=f"{drone}: {data['Active']} | {data['Battery Life']} | Speed: {data['Drone Speed']}",
            icon=folium.Icon(color="blue")
        ).add_to(m)

    for fire, data in st.session_state.fire_data.items():
        folium.Marker(
            location=data["Coords"],
            popup=f"{fire}: Type: {data['Type']} | Size: {data['Size']} | Temp: {data['Temperature']}",
            icon=folium.Icon(color="red")
        ).add_to(m)

    for base, data in st.session_state.base_data.items():
        folium.Marker(
            location=data["Coords"],
            popup=f"{base}: Suppressants: {data['Suppressant Tank']} | Water: {data['Water Tank']}",
            icon=folium.Icon(color="green")
        ).add_to(m)

elif selected_layer == "Topographical":
    m = folium.Map(location=[0, 0], zoom_start=2, tiles="Stamen Terrain")

elif selected_layer == "Wind":
    m = folium.Map(location=[0, 0], zoom_start=2, tiles="OpenStreetMap")
    plugins.FloatImage("https://i.imgur.com/Q8ZCzrX.png", bottom=10, left=10).add_to(m)

elif selected_layer == "Heat":
    m = folium.Map(location=[0, 0], zoom_start=2)
    heat_data = [data["Coords"] for data in st.session_state.fire_data.values()]
    plugins.HeatMap(heat_data).add_to(m)

#display map
st.components.v1.html(m._repr_html_(), height=500)

st.markdown("---")
col1, col2 = st.columns(2)
# with col1:
#     st.button("Terminate Selected")
# with col2:
#     st.button("Terminate All")

