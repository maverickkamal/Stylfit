import streamlit as st
from tavily import TavilyClient
import requests
import os


def get_weather(city: str) -> str:
    """
    Fetches the current weather information for a given city.

    This function retrieves the weather data from the WeatherAPI service by sending a request to their API using the
    specified city name. It uses an API key stored in the environment variables for authentication. The function
    returns the weather data in JSON format or an error message if the request fails.

    Args:
        city (str): The name of the city for which the weather information is to be retrieved.

    Returns:
        str: A JSON string containing the current weather data or an error message if the request fails.
    """
    API_KEY = st.secrets["WEATHER_API_KEY"]

    url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}'

    try:
        response = requests.get(url)
        print('checked...')

        return response.json()
    except Exception as e:
        return f"An error occurred: {e}"

        
def search_web(query: str) -> str:
    """
    Searches the web using the Tavily API for the given query.

    Args:
        query (str): The search query.

    Returns:
        str: The search results in JSON format.
    """
    
    client = TavilyClient(api=st.secrets["TAVILY_API_KEY"])
    search_results = client.search(query=query)
    return search_results
    
