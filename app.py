import gradio as gr
import requests

# Some example European cities
CITIES = {
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Rome": (41.9028, 12.4964),
    "Madrid": (40.4168, -3.7038),
    "Zurich": (47.3769, 8.5417),
}

def get_climate_risk(city_name: str) -> str:
    lat, lon = CITIES[city_name]

    # Call Open-Meteo API for hourly temperature
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return f"Error fetching data: {e}"

    data = resp.json()
    temps = data["hourly"]["temperature_2m"]
    times = data["hourly"]["time"]

    if not temps:
        return "No temperature data available."

    current_temp = temps[-1]
    current_time = times[-1]

    # Very simple heat risk logic for demo
    if current_temp >= 35:
        risk = "High heat risk 🥵"
    elif current_temp >= 28:
        risk = "Moderate heat risk 😓"
    else:
        risk = "Low heat risk 🙂"

    result = (
        f"City: {city_name}\n"
        f"Time (UTC): {current_time}\n"
        f"Current temperature: {current_temp} °C\n"
        f"Risk level: {risk}"
    )
    return result

demo = gr.Interface(
    fn=get_climate_risk,
    inputs=gr.Dropdown(choices=list(CITIES.keys()), label="City"),
    outputs=gr.Textbox(label="Climate risk"),
    title="European Heat Risk Demo",
    description="Select a city and get a simple heat risk based on current temperature.",
)

if __name__ == "__main__":
    demo.launch()

