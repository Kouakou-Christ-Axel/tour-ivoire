from app.ai.tools import get_pois
from app.ai.tools.suggest_cities import suggest_cities_rag
from langchain_core.tools import tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper

weather = OpenWeatherMapAPIWrapper()

agent_tools = [
    suggest_cities_rag,
    weather.run,
    # get_pois
]

def get_weather_forecast(location: str) -> str:
    """Get the weather forecast for a given location.

    Args:
        location (str): The location to get the weather forecast for (e.g., "New York City").

    Returns:
        str: A mock weather forecast for the specified location.
    """
    # In a real implementation, this function would call an external API
    # such as OpenWeatherMap API, WeatherAPI, etc. to get real data.
    # Here, we return a mock response for demonstration purposes.

    mock_weather = {
        "New York City": "Sunny, 75°F",
        "San Francisco": "Foggy, 60°F",
        "Los Angeles": "Sunny, 85°F",
        "Chicago": "Cloudy, 70°F"
    }

    weather = mock_weather.get(location, "Weather data not available for this location.")
    return f"The current weather in {location} is: {weather}"