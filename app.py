import streamlit as st
import requests

st.title("European Climate Risk Demo")

st.write("Simple demo: enter a location and see a basic heat risk from current temperature.")

cities = {
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Rome": (41.9028, 12.4964),
    "Madrid": (40.4168, -3.7038),
    "Zurich": (47.3769, 8.5417),
}

city = st.selectbox("Choose a city", list(cities.keys()))
lat, lon = cities[city]

st.write(f"Selected: {city} (lat={lat}, lon={lon})")

if st.button("Get current climate risk"):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        st.error("Error fetching data from API")
    else:
        data = resp.json()
        temps = data["hourly"]["temperature_2m"]
        times = data["hourly"]["time"]

        current_temp = temps[-1]
        st.write(f"Current temperature: **{current_temp} °C**")

        if current_temp >= 35:
            risk = "High heat risk 🥵"
        elif current_temp >= 28:
            risk = "Moderate heat risk 😓"
        else:
            risk = "Low heat risk 🙂"

        st.write(f"Risk level: **{risk}**")

        st.write("Recent temperatures:")
        st.line_chart({"temperature_2m": temps[-24:]})
