# weather_server.py
from fastmcp import FastMCP
import requests

# ➊ Instantiate your MCP server
mcp = FastMCP("WeatherServer")

# ➋ Register get_weather
@mcp.tool
def get_weather(lat: float, lon: float) -> float:
    """Return current temperature (°C) via Open-Meteo."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["current_weather"]["temperature"]

# ➌ Register convert_c_to_f
@mcp.tool
def convert_c_to_f(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return c * 9/5 + 32

# ➍ Run the server
if __name__ == "__main__":
    # Serve over HTTP on 127.0.0.1:8000, JSON-RPC path "/mcp/"
    mcp.run(
        transport="http", 
        host="127.0.0.1", 
        port=8000,
        path="/mcp/"         # this is the default; you can omit it
    )
