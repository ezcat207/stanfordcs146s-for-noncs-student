"""
Demo MCP Server: Weather API Wrapper
This shows how to build a custom MCP server that wraps an external API.
Target audience: Complete beginners (18-year-olds with no CS background)
"""
from typing import Any, Dict
from fastmcp import FastMCP
import httpx  # Modern HTTP client library

# Initialize our MCP server with a descriptive name
mcp = FastMCP(name="WeatherMCPServer")

# API Configuration - In real apps, use environment variables!
WEATHER_API_BASE = "https://api.open-meteo.com/v1"

@mcp.tool
def get_current_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Gets the current weather for a specific location.

    :param latitude: Latitude coordinate (e.g., 37.7749 for San Francisco)
    :param longitude: Longitude coordinate (e.g., -122.4194 for San Francisco)
    :return: Current weather conditions including temperature and conditions
    """
    try:
        # Build the API request URL
        url = f"{WEATHER_API_BASE}/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true"
        }

        # Make the HTTP request to the external API
        response = httpx.get(url, params=params, timeout=10.0)

        # Check if the request was successful
        if response.status_code != 200:
            return {
                "error": f"API returned status code {response.status_code}",
                "location": f"{latitude}, {longitude}"
            }

        # Parse the JSON response
        data = response.json()
        current = data.get("current_weather", {})

        return {
            "location": f"{latitude}, {longitude}",
            "temperature_celsius": current.get("temperature"),
            "wind_speed_kmh": current.get("windspeed"),
            "weather_code": current.get("weathercode"),
            "timestamp": current.get("time")
        }

    except httpx.TimeoutException:
        return {
            "error": "Request timed out - the weather API took too long to respond",
            "location": f"{latitude}, {longitude}"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "location": f"{latitude}, {longitude}"
        }

@mcp.tool
def get_city_coordinates(city_name: str) -> Dict[str, Any]:
    """
    Gets the latitude and longitude for a city name.
    This is a simplified version - in production, use a geocoding API.

    :param city_name: Name of the city (e.g., "San Francisco", "New York")
    :return: Latitude and longitude coordinates
    """
    # Hardcoded city database (in real apps, use a geocoding API)
    cities = {
        "san francisco": {"lat": 37.7749, "lon": -122.4194},
        "new york": {"lat": 40.7128, "lon": -74.0060},
        "london": {"lat": 51.5074, "lon": -0.1278},
        "tokyo": {"lat": 35.6762, "lon": 139.6503},
        "paris": {"lat": 48.8566, "lon": 2.3522}
    }

    city_lower = city_name.lower()
    if city_lower in cities:
        coords = cities[city_lower]
        return {
            "city": city_name,
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "found": True
        }
    else:
        return {
            "city": city_name,
            "found": False,
            "error": f"City '{city_name}' not found in database",
            "available_cities": list(cities.keys())
        }

# This is how we run the MCP server
if __name__ == "__main__":
    mcp.run()
