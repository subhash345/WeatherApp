import requests
import streamlit as st
from datetime import datetime

def get_current_weather(city):
    api_key = "c42a09c1a3e8685b4d0cbfda38c22023"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors
    except requests.exceptions.HTTPError as err:
        st.error(f"Error: {err}")
        return None, None
    
    try:
        data = response.json()
        if data['cod'] != 200:
            st.error(f"Error: {data['message']}")
            return None, None
    except json.JSONDecodeError as err:
        st.error(f"Error: Failed to parse response JSON - {err}")
        return None, None
    
    # Extract relevant current weather information
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    weather_desc = data['weather'][0]['description']
    pressure = data['main']['pressure']
    
    # Convert temperature from Kelvin to Celsius
    temperature = round(temperature, 2)
    
    # Fetch weather forecast data
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()  # Raise an exception for any HTTP errors
    except requests.exceptions.HTTPError as err:
        st.error(f"Error fetching forecast: {err}")
        return None, None
    
    try:
        forecast_data = forecast_response.json()
        if forecast_data['cod'] != '200':
            st.error(f"Error fetching forecast: {forecast_data['message']}")
            return None, None
    except json.JSONDecodeError as err:
        st.error(f"Error parsing forecast JSON: {err}")
        return None, None
    
    # Extract relevant forecast data for the next 5 hours
    forecast_table = {'Time': [], 'Temperature (°C)': [], 'Weather': []}
    for forecast in forecast_data['list'][:5]:
        forecast_time = datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
        forecast_temp = forecast['main']['temp']
        forecast_weather = forecast['weather'][0]['description']
        
        forecast_table['Time'].append(forecast_time)
        forecast_table['Temperature (°C)'].append(round(forecast_temp, 2))
        forecast_table['Weather'].append(forecast_weather)
    
    return (temperature, humidity, weather_desc, pressure), forecast_table

# Streamlit UI
st.markdown("<h1 style='color: white; font-family: Copperplate Gothic Bold;'>🌤️ Weather Forecasting Application</h1>", unsafe_allow_html=True)

city = st.text_input("Enter city name")
if st.button("Get Weather"):
    current_weather, forecast_table = get_current_weather(city)
    if current_weather and forecast_table:
        temperature, humidity, weather_desc, pressure = current_weather
        
        # Display current weather information in tabular form
        st.write("Current Weather:")
        current_weather_table = {
            'Temperature (°C)': [temperature],
            'Humidity (%)': [humidity],
            'Weather': [weather_desc],
            'Pressure (hPa)': [pressure]
        }
        st.table(current_weather_table)
        
        # Display weather forecast for the next 5 hours in tabular form
        st.write("Weather Forecast for the Next 5 Hours:")
        st.table(forecast_table)