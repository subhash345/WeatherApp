# Importing necessary libraries
import requests
import streamlit as st
import json
from datetime import datetime

# Function to retrieve current weather and forecast data for a given city
def get_current_weather(city):
    # API key for OpenWeatherMap API
    api_key = "c42a09c1a3e8685b4d0cbfda38c22023"
    
    # URL for current weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        # Sending request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors
    except requests.exceptions.HTTPError as err:
        st.error(f"Error: {err}")
        return None, None
    
    try:
        # Parsing response JSON
        data = response.json()
        if data['cod'] != 200:
            st.error(f"Error: {data['message']}")
            return None, None
    except json.JSONDecodeError as err:
        st.error(f"Error: Failed to parse response JSON - {err}")
        return None, None

    # Extracting current weather data
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    weather_desc = data['weather'][0]['description']
    pressure = data['main']['pressure']
    
    temperature = round(temperature, 2)
    
    # URL for weather forecast data
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        # Sending request to the API
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()  # Raise an exception for any HTTP errors
    except requests.exceptions.HTTPError as err:
        st.error(f"Error fetching forecast: {err}")
        return None, None
    
    try:
        # Parsing forecast response JSON
        forecast_data = forecast_response.json()
        if forecast_data['cod'] != '200':
            st.error(f"Error fetching forecast: {forecast_data['message']}")
            return None, None
    except json.JSONDecodeError as err:
        st.error(f"Error parsing forecast JSON: {err}")
        return None, None
    
    # Creating forecast table to store forecast data
    forecast_table = {'Date': [], 'Temperature (°C)': [], 'Humidity (%)': [], 'Pressure (hPa)': [], 'Weather': []}
    today = datetime.utcnow().date()
    for forecast in forecast_data['list']:
        forecast_date = datetime.utcfromtimestamp(forecast['dt']).date()
        if forecast_date != today:
            forecast_temp = forecast['main']['temp']
            forecast_humidity = forecast['main']['humidity']
            forecast_pressure = forecast['main']['pressure']
            forecast_weather = forecast['weather'][0]['description']
            
            # Adding forecast data to forecast table
            forecast_table['Date'].append(forecast_date.strftime('%Y-%m-%d'))
            forecast_table['Temperature (°C)'].append(round(forecast_temp, 2))
            forecast_table['Humidity (%)'].append(forecast_humidity)
            forecast_table['Pressure (hPa)'].append(forecast_pressure)
            forecast_table['Weather'].append(forecast_weather)
            today = forecast_date
    
    return (temperature, humidity, weather_desc, pressure), forecast_table

# Setting Streamlit page configuration
st.set_page_config(page_title="Weather Forecasting Application", page_icon="🌤️")
st.markdown("<h1 style='color: white; font-family: Copperplate Gothic Bold;'>🌤️ Weather Forecasting Application</h1>", unsafe_allow_html=True)

# Add background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://images.pexels.com/photos/1592263/pexels-photo-1592263.jpeg");
        background-size: cover;
        background-position: center;
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Text input field for entering city name
city = st.text_input("Enter city name")

# Button to trigger weather retrieval
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
        
        # Display weather forecast for the next 5 days in tabular form
        st.write("Weather Forecast for the Next 5 Days:")
        st.table(forecast_table)
