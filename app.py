import requests
import streamlit as st

def get_current_weather(city):
    api_key = "c42a09c1a3e8685b4d0cbfda38c22023"
    url = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors
    except requests.exceptions.HTTPError as err:
        st.error(f"Error: {err}")
        return None