import streamlit as st
import random
import folium
from folium import plugins
import websockets
import asyncio
import json


async def connect_to_websocket():
    while True:
        selected_drone = st.session_state.get("selected_drone")
        sidebar_drone = st.session_state.get("sidebar_drone")

        if not selected_drone:
            await asyncio.sleep(1)
            continue

        currently_selected_drone = selected_drone
        uri = f"ws://localhost:8000/ws/{currently_selected_drone}"

        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    print(f"Getting data for drone {currently_selected_drone}")
                    data = await websocket.recv()
                    st.session_state.drone_data[currently_selected_drone] = json.loads(data)

                    if selected_drone == currently_selected_drone:
                        text_area = "\n".join(
                            f"{key}: {value}" for key, value in st.session_state.drone_data[currently_selected_drone].items()
                        )
                        sidebar_drone.text(text_area)
                    else:
                        await websocket.close()
                        print(f"Stopped getting data for drone {currently_selected_drone}")
                        break
                except websockets.exceptions.ConnectionClosed:
                    print(f"Connection closed for drone {currently_selected_drone}")
                    break
                await asyncio.sleep(1)


def get_drone_data():
    return {
        "Battery Life": f"100%",
        "Drone Speed": f"{random.randint(0, 100)} m/s",
        "Coords": (random.uniform(-90, 90), random.uniform(-180, 180)),
        "Suppressant Level": f"{random.randint(0, 100)}%",
        "Active": random.choice(["Moving", "Idle"]),
        "Suppressing": random.choice(["Yes", "No"])
    }


def get_fire_data():
    return {
        "Coords": (random.uniform(-90, 90), random.uniform(-180, 180)),
        "Type": random.choice(["Wildfire", "Campfire"]),
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


def initialize_session_state():
    if "drone_data" not in st.session_state:
        st.session_state.drone_data = {f"Drone{i}": get_drone_data() for i in range(1, 5)}

    if "fire_data" not in st.session_state:
        st.session_state.fire_data = {f"Fire {i}": get_fire_data() for i in range(1, 5)}

    if "base_data" not in st.session_state:
        st.session_state.base_data = {f"Base {i}": get_base_data() for i in range(1, 5)}


async def main():
    initialize_session_state()

    st.sidebar.header("Select Drone")
    drone_options = list(st.session_state.drone_data.keys())
    st.session_state.selected_drone = st.sidebar.selectbox("Choose a drone to view data:", drone_options)
    st.session_state.sidebar_drone = st.sidebar.empty()

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
    st.subheader("Maps")
    layer_options = ["Station + Drone + Fire", "Topographical", "Wind", "Heat"]
    selected_layer = st.selectbox("Choose a layer to display:", layer_options)

    #map
    center_coords = (0, 0)
    if selected_layer == "Station + Drone + Fire":
        m = folium.Map(location=center_coords, zoom_start=2)
        for drone, data in st.session_state.drone_data.items():
            folium.Marker(location=data["Coords"], popup=f"{drone}: {data['Active']}", icon=folium.Icon(color="blue")).add_to(m)
        for fire, data in st.session_state.fire_data.items():
            folium.Marker(location=data["Coords"], popup=f"{fire}: {data['Type']}", icon=folium.Icon(color="red")).add_to(m)
        for base, data in st.session_state.base_data.items():
            folium.Marker(location=data["Coords"], popup=f"{base}: {data['Suppressant Tank']}", icon=folium.Icon(color="green")).add_to(m)

    elif selected_layer == "Topographical":
        m = folium.Map(location=center_coords, zoom_start=2, tiles="Stamen Terrain")
    elif selected_layer == "Wind":
        m = folium.Map(location=center_coords, zoom_start=2)
        plugins.FloatImage("https://i.imgur.com/Q8ZCzrX.png", bottom=10, left=10).add_to(m)
    elif selected_layer == "Heat":
        heat_data = [data["Coords"] for data in st.session_state.fire_data.values()]
        m = folium.Map(location=center_coords, zoom_start=2)
        plugins.HeatMap(heat_data).add_to(m)

    st.components.v1.html(m._repr_html_(), height=500)


if __name__ == "__main__":
    asyncio.run(main())

