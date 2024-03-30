import requests
import json
import streamlit as st

def get_current_weather(city):
    api_key = "c42a09c1a3e8685b4d0cbfda38c22023"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors
    except requests.exceptions.HTTPError as err:
        st.error(f"Error: {err}")
        return None
    
    try:
        data = response.json()
        if data['cod'] != 200:
            st.error(f"Error: {data['message']}")
            return None
    except json.JSONDecodeError as err:
        st.error(f"Error: Failed to parse response JSON - {err}")
        return None
    
    # Extract relevant weather information
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    weather_desc = data['weather'][0]['description']
    pressure = data['main']['pressure']
    
    # Convert temperature from Kelvin to Celsius
    temperature = round(temperature, 2)
    
    return temperature, humidity, weather_desc, pressure

# Streamlit UI
st.markdown("<h1 style='color: white; font-family: Copperplate Gothic Bold;'>🌤️ Weather Forecasting Application</h1>", unsafe_allow_html=True)

city = st.text_input("Enter city name")
if st.button("Get Weather"):
    weather_data = get_current_weather(city)
    if weather_data:
        temperature, humidity, weather_desc, pressure = weather_data
        
        # Display weather information in tabular form
        weather_table = {
            'Temperature (°C)': [temperature],
            'Humidity (%)': [humidity],
            'Weather': [weather_desc],
            'Pressure (hPa)': [pressure]
        }
        st.table(weather_table)