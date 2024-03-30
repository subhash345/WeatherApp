import requests
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
        
    # Extract relevant current weather information
    temperature = data['main']['temp']
    
    # Convert temperature from Kelvin to Celsius
    temperature = round(temperature, 2)
    
    return temperature

st.markdown("<h1 style='color: red; font-family: Italic Bold;'> Weather Forecasting Application</h1>", unsafe_allow_html=True)

city = st.text_input("Enter city name")
if st.button("Get Weather"):
    current_temperature = get_current_weather(city)
    if current_temperature:
        st.write(f"Temperature: {current_temperature}°C")
