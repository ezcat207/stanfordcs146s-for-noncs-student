# Lecture Transcript: Building Your First Custom MCP Server

**Date:** Week 3 - Fall 2025
**Topic:** Building a Custom MCP Server with External APIs
**Based on:** Lecture slides and `weather_mcp_demo.py`
**Target Audience:** Complete beginners (18-year-olds with no CS background)

---

## Introduction: From Learning to Building

"Welcome to Week 3! Last week, we learned **what** MCP is and **why** it matters. We saw how MCP is like USB-C for AI—a universal standard that lets AI systems talk to any data source without custom code for each one.

But here's the thing: we only used MCP servers that already existed. We plugged them in and used them. That's useful, but it's like only knowing how to use apps on your phone without understanding how to build them.

This week, we're going to **build our own MCP server from scratch.** And not just any server—we're going to build one that connects to a real external API, bringing live data from the internet into your AI assistant.

By the end of this lecture, you'll understand how to wrap any API (weather, GitHub, Spotify, whatever you want) and make it available to Claude or any other AI system."

---

## The Big Picture: What We're Building Today

"Let's start with the 'why' before the 'how.'

**The Problem:**
You're chatting with Claude and you ask: 'What's the weather like in San Francisco right now?'

Claude has a problem. It's a language model—it only knows patterns from text it was trained on. It doesn't have a live connection to weather data. It can't check the current temperature. It would have to say, 'I don't know, I don't have access to current weather data.'

**The Solution:**
We build an **MCP server** that acts as a bridge between Claude and a weather API.

Think of it like this:
- **Claude** is the brain 🧠
- **Weather API** is the weather station 🌤️
- **Our MCP Server** is the translator/messenger 📱

Claude speaks 'AI language' (JSON, tool calls, structured data).
The Weather API speaks 'HTTP language' (REST endpoints, query parameters).
Our MCP server sits in the middle and translates both ways.

When Claude wants weather data:
1. Claude asks: 'get_current_weather(San Francisco)'
2. Our MCP server translates: 'GET https://api.weather.com?city=San Francisco'
3. Weather API responds: '{temp: 72, conditions: sunny}'
4. Our MCP server translates back: 'Temperature is 72°F, sunny'
5. Claude receives the data and can answer the user

**That's what we're building today.**"

---

## Analogy: MCP Server as a Restaurant Menu

"Before we dive into code, let me give you an analogy that will make everything click.

**Your MCP Server is like a Restaurant Menu.**

When you go to a restaurant, you don't go into the kitchen and start cooking. You don't need to know how the chef makes the pasta. You just look at the menu and say, 'I'll have the carbonara, please.'

The menu does three things:
1. **Lists what's available** (Tools: 'Carbonara,' 'Margherita Pizza,' 'Caesar Salad')
2. **Describes each dish** (Tool descriptions: 'Classic Italian pasta with eggs and bacon')
3. **Takes your order and delivers the food** (Execution: kitchen makes it, waiter brings it)

**That's exactly what an MCP server does for Claude:**
1. **Lists what's available** ('get_current_weather,' 'get_city_coordinates')
2. **Describes each tool** ('Gets current weather for a location')
3. **Takes Claude's request and delivers the result** (Calls the weather API, returns data)

The genius of MCP is that **every MCP server has the same menu format.** Whether it's weather, GitHub, or Spotify, Claude knows how to read the menu because they all follow the same standard. That's the power of MCP."

---

## Code Walkthrough: Building the Weather MCP Server

"Now let's build this thing. Open up `weather_mcp_demo.py` and let's go through it line by line.

### Part 1: The Imports (Lines 1-7)

```python
from typing import Any, Dict
from fastmcp import FastMCP
import httpx  # Modern HTTP client library
```

**What's happening here?**
- `typing`: Lets us tell Python what kind of data we're working with (like saying 'this variable is a number')
- `fastmcp`: The library that makes building MCP servers super easy
- `httpx`: A library for making HTTP requests to external APIs (like fetching data from websites)

**Analogy:** These are your tools. Like a carpenter grabs a hammer and saw before building a chair, we grab these libraries before building our server.

### Part 2: Initialize the Server (Line 10)

```python
mcp = FastMCP(name='WeatherMCPServer')
```

**What's happening?**
We create an instance of FastMCP. This is the foundation of our server—everything else builds on top of this.

**Important:** The `name` field is how Claude (or any client) will identify our server. Choose something descriptive.

**Analogy:** This is like hanging a sign on your restaurant: 'Joe's Pizza Place.' Now people know what you do.

### Part 3: Our First Tool - get_current_weather (Lines 15-60)

```python
@mcp.tool
def get_current_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    \"\"\"
    Gets the current weather for a specific location.

    :param latitude: Latitude coordinate (e.g., 37.7749 for San Francisco)
    :param longitude: Longitude coordinate (e.g., -122.4194 for San Francisco)
    :return: Current weather conditions including temperature and conditions
    \"\"\"
```

**The Magic: @mcp.tool**

This `@mcp.tool` decorator is **the most important line in the entire file.**

Here's what it does:
1. It tells FastMCP: 'Hey, this function is a tool that Claude can call'
2. FastMCP automatically reads the function name, parameters, and docstring
3. It generates a JSON schema (the 'menu item') that describes this tool to Claude
4. When Claude calls `get_current_weather(37.7749, -122.4194)`, FastMCP routes it to this function

**You don't have to write any JSON manually.** The decorator handles everything.

**Analogy:** It's like telling the restaurant owner, 'Add this dish to the menu.' The owner automatically creates the menu description, sets the price, and trains the waiter. You just make the dish.

### Part 4: Making the HTTP Request (Lines 22-32)

```python
url = f'{WEATHER_API_BASE}/forecast'
params = {
    'latitude': latitude,
    'longitude': longitude,
    'current_weather': 'true'
}

response = httpx.get(url, params=params, timeout=10.0)
```

**What's happening?**
1. We build the URL for the weather API
2. We create a dictionary of parameters (latitude, longitude, etc.)
3. We use `httpx.get()` to make an HTTP GET request to the API

**What's an HTTP GET request?**
It's how your computer asks a website for data. When you visit `google.com` in your browser, your browser makes a GET request. Same concept here.

**The `timeout=10.0` part:** We're saying, 'If the API doesn't respond in 10 seconds, give up.' This prevents our server from hanging forever if the API is slow.

**Analogy:** Making an HTTP request is like calling a pizza place to order delivery. You dial (the URL), you tell them your order (the parameters), and you wait for them to answer (the response). If they don't pick up in 10 seconds, you hang up.

### Part 5: Error Handling (Lines 35-39, 50-60)

```python
if response.status_code != 200:
    return {
        'error': f'API returned status code {response.status_code}',
        'location': f'{latitude}, {longitude}'
    }
```

**What's a status code?**
When an API responds, it sends a number:
- `200` = Success! Everything worked
- `404` = Not found (like clicking a broken link)
- `500` = Server error (the API's computer crashed)

We check if the status code is `200`. If not, we return an error message instead of crashing.

**Why is this important?**
External APIs fail all the time. The internet is unreliable. Your code needs to handle failure gracefully.

**Real-world example:** Imagine Claude is helping a user plan a trip and it needs weather data. If the weather API is down and we don't handle errors, Claude would crash. Instead, we return a nice error message: 'Sorry, the weather API is unavailable right now.'

**The try/except block (Lines 22-60):**
```python
try:
    # Try to do this
except httpx.TimeoutException:
    # If it times out, do this
except Exception as e:
    # If anything else goes wrong, do this
```

This is Python's way of saying, 'Try to run this code. If something goes wrong, don't crash—handle it.'

**Analogy:** It's like having a backup plan. You try to order pizza. If they're closed (timeout), you order Chinese food instead. If Chinese is also closed (exception), you make a sandwich.

### Part 6: Parsing the Response (Lines 42-49)

```python
data = response.json()
current = data.get('current_weather', {})

return {
    'location': f'{latitude}, {longitude}',
    'temperature_celsius': current.get('temperature'),
    'wind_speed_kmh': current.get('windspeed'),
    'weather_code': current.get('weathercode'),
    'timestamp': current.get('time')
}
```

**What's happening?**
1. `response.json()` converts the API's text response into a Python dictionary
2. We extract the `current_weather` field from the data
3. We build a clean, structured dictionary to return to Claude

**Why build a new dictionary?**
The API's response might have 50 fields we don't care about. We only extract the important ones and package them nicely for Claude.

**Analogy:** The weather API sends us a giant encyclopedia. We read it, highlight the important parts (temperature, wind speed), and hand Claude a simple summary.

### Part 7: The Second Tool - get_city_coordinates (Lines 63-94)

```python
@mcp.tool
def get_city_coordinates(city_name: str) -> Dict[str, Any]:
    \"\"\"
    Gets the latitude and longitude for a city name.
    \"\"\"
    cities = {
        'san francisco': {'lat': 37.7749, 'lon': -122.4194},
        'new york': {'lat': 40.7128, 'lon': -74.0060},
        # ...
    }
```

**Why do we need this?**
The weather API requires latitude and longitude. But users think in city names ('San Francisco'), not coordinates ('37.7749, -122.4194').

This tool acts as a **lookup table**—you give it 'San Francisco,' it gives you the coordinates.

**Note:** This is a simplified version with hardcoded cities. In a real app, you'd use a geocoding API (like Google Maps API) to look up any city in the world.

**Analogy:** It's like a phone book. You know your friend's name (city), you look it up in the phone book (this function), and you get their phone number (coordinates).

### Part 8: Running the Server (Lines 97-98)

```python
if __name__ == '__main__':
    mcp.run()
```

**What does this do?**
When you run `python weather_mcp_demo.py` in your terminal, this line starts the MCP server. It sits there, waiting for Claude (or any MCP client) to connect.

**What's `if __name__ == '__main__'`?**
This is Python's way of saying, 'Only run this code if someone is running this file directly (not importing it as a library).'

**How does Claude connect?**
You'd add this to your Claude Desktop config:
```json
{
  'mcpServers': {
    'weather': {
      'command': 'python',
      'args': ['/path/to/weather_mcp_demo.py']
    }
  }
}
```

Now when you open Claude Desktop, it automatically starts your server in the background."

---

## Putting It All Together: The Flow

"Let's trace what happens when a user asks Claude: 'What's the weather in San Francisco?'

**Step 1:** User types the question
**Step 2:** Claude thinks: 'I need weather data. Let me check my tools...'
**Step 3:** Claude sees `get_current_weather` in the WeatherMCPServer menu
**Step 4:** But wait—it needs coordinates, not a city name
**Step 5:** Claude sees `get_city_coordinates` tool
**Step 6:** Claude calls: `get_city_coordinates('San Francisco')`
**Step 7:** Our server returns: `{lat: 37.7749, lon: -122.4194}`
**Step 8:** Claude calls: `get_current_weather(37.7749, -122.4194)`
**Step 9:** Our server makes HTTP request to weather API
**Step 10:** Weather API returns: `{temp: 72, windspeed: 15}`
**Step 11:** Our server packages it nicely and returns to Claude
**Step 12:** Claude responds to user: 'It's 72°F and sunny in San Francisco!'

**Notice something?** Claude made **two** tool calls. It figured out on its own that it needed to convert city→coordinates first. **You didn't tell it to do that.** The AI is smart enough to chain tools together.

**That's the power of well-designed tools with good descriptions.**"

---

## Key Principles for Building MCP Servers

"Before we wrap up, let me give you the **golden rules** for building production-quality MCP servers:

### 1. Always Handle Errors
External APIs fail. Networks fail. Users enter invalid data. Your code must handle every failure case gracefully. Use try/except blocks. Return helpful error messages.

### 2. Use Clear Names and Descriptions
Your function names and docstrings are **the interface** between your code and the AI. Make them crystal clear. Compare:
- **Bad:** `def get_data(x, y)`
- **Good:** `def get_current_weather(latitude: float, longitude: float)`

The AI reads your docstring to understand what the tool does. Write it for the AI, not for humans.

### 3. Return Structured Data
Always return dictionaries with clear keys. Don't return raw strings. Compare:
- **Bad:** `return '72 degrees'`
- **Good:** `return {'temperature': 72, 'unit': 'fahrenheit'}`

Structured data is easier for the AI to parse and use.

### 4. Respect Rate Limits
Most APIs have rate limits (e.g., '100 requests per hour'). If you exceed them, the API blocks you. Add logic to track requests or warn users.

### 5. Never Hardcode Secrets
In our demo, we used a public weather API with no API key. But most APIs require authentication. **Never** put API keys directly in your code. Use environment variables:

```python
import os
API_KEY = os.getenv('WEATHER_API_KEY')
```

Then set it in your shell:
```bash
export WEATHER_API_KEY='your-secret-key'
```

### 6. Use Type Hints
Notice how we wrote `latitude: float` instead of just `latitude`? Those are **type hints**. They tell Python (and MCP) what kind of data to expect. This prevents bugs and helps with auto-generation of tool schemas.

### 7. Test Your Tools Manually First
Before hooking your server to Claude, test it standalone:
```python
result = get_current_weather(37.7749, -122.4194)
print(result)
```

Make sure it works before integrating with MCP."

---

## What's Next: Your Assignment

"Now you know how to build a custom MCP server. For your assignment, you'll:
1. Pick an external API (weather, GitHub, Spotify, whatever interests you)
2. Build an MCP server with at least 2 tools
3. Handle errors gracefully
4. Write clear documentation

The world has thousands of public APIs. You can wrap any of them. Want to let Claude check movie ratings? Use the OMDB API. Want Claude to create GitHub issues? Use the GitHub API. Want Claude to search for recipes? Use the Spoonacular API.

**The pattern is always the same:**
1. Make HTTP request to external API
2. Parse the response
3. Return structured data to Claude

You've learned the template today. Now apply it to something that excites you."

---

## Conclusion: You're Now a Builder, Not Just a User

"When you started this course, you were a **user** of AI. You typed prompts and got responses.

After Week 1, you became a **power user**—you understood how to structure prompts, use few-shot learning, and get better results.

After Week 2, you became a **integrator**—you understood how to connect AI to tools using MCP.

Today, Week 3, you became a **builder**—you can create new capabilities and share them with the world.

That's the journey. From consumer to creator.

Here's the thing: there are millions of APIs out there. Most of them don't have MCP servers yet. **You can build them.** You can be the person who makes Spotify, or Notion, or your school's student portal available to AI systems. You can publish your server on GitHub and other people can use it.

That's the modern software developer mindset: See a gap. Build the bridge. Share it.

See you next week."

---

## Appendix: Common Mistakes to Avoid

1. **Forgetting error handling:** Your code will crash the first time the API is down
2. **Using `print()` for logging in MCP servers:** Use proper logging libraries instead
3. **Not reading the API documentation:** Every API is different; read the docs first
4. **Returning inconsistent data structures:** Claude expects the same format every time
5. **Ignoring rate limits:** You'll get blocked by the API
6. **Hardcoding file paths or API keys:** Use environment variables and relative paths

---

## Additional Resources

- MCP Official Documentation: https://modelcontextprotocol.io
- FastMCP GitHub: https://github.com/jlowin/fastmcp
- Public APIs List: https://github.com/public-apis/public-apis
- httpx Documentation: https://www.python-httpx.org/
- Python Type Hints Guide: https://docs.python.org/3/library/typing.html
