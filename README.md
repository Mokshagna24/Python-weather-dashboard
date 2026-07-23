# Python Async Weather Dashboard

A command-line weather and air quality dashboard built with Python.
Fetches live data for multiple Indian cities simultaneously using
async HTTP requests — all in under 0.5 seconds.

## Features

- Live weather data: temperature, humidity, wind speed
- Live air quality index (AQI) with health status
- Async requests with aiohttp — all cities fetched in parallel
- Per-city error handling with automatic retry
- Clean formatted terminal output
  
## Tech stack

- Python 3.13
- aiohttp — async HTTP client
- asyncio — Python async framework
- Open-Meteo API — free weather + air quality data (no API key needed)

## Setup

```bash
# Clone the repo
git clone https://github.com/Mokshagna24/python-weather-dashboard.git
cd python-weather-dashboard

# Create and activate virtual environment
python -m venv env
env\Scripts\activate        # Windows
source env/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python dashboard.py
```

Expected output:

```
  Weather + Air Quality Dashboard
  20 May 2026  16:30
  ──────────────────────────────────────

  City          Temp  Humidity   Wind  AQI  Status
  ──────────────────────────────────────
  Hyderabad    34°C      42%  12km/h   58  Moderate
  Mumbai       32°C      78%   8km/h   44  Good
  Delhi        39°C      22%  15km/h  142  Unhealthy
  Chennai      33°C      68%  14km/h   51  Moderate
  Bangalore    28°C      55%   6km/h   38  Good

  Fetched 5 cities in 0.31s
```

## Project structure

```
python-weather-dashboard/
├── dashboard.py          # main async dashboard script
├── weather_with_async.py # async weather fetcher
├── requirements.txt      # pinned dependencies
├── .gitignore            # excludes env/ and __pycache__
└── README.md             # this file
```

## What I learned

Built this project to practise:
- Python virtual environments and dependency management
- REST API calls with the requests library
- Async programming with asyncio and aiohttp
- Git version control and GitHub

## Author

Mokshagna24 — [GitHub](https://github.com/Mokshagna24)
