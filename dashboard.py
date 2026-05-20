import asyncio
import aiohttp
import time
from datetime import datetime

CITIES = [
    {"name": "Hyderabad", "lat": 17.38, "lon": 78.47},
    {"name": "Mumbai",    "lat": 19.07, "lon": 72.87},
    {"name": "Delhi",     "lat": 28.67, "lon": 77.22},
    {"name": "Chennai",   "lat": 13.08, "lon": 80.27},
    {"name": "Bangalore", "lat": 12.97, "lon": 77.59},
]

WEATHER_URL   = "https://api.open-meteo.com/v1/forecast"
AIR_URL       = "https://air-quality-api.open-meteo.com/v1/air-quality"
TIMEOUT       = aiohttp.ClientTimeout(total=8)

async def fetch_weather(session, city, retries=2):
    params = {
        "latitude":  city["lat"],
        "longitude": city["lon"],
        "current":   "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }
    for attempt in range(retries):
        try:
            async with session.get(WEATHER_URL, params=params, timeout=TIMEOUT) as r:
                r.raise_for_status()
                return (await r.json())["current"]
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(1)   # wait 1s then retry
            else:
                return {"error": str(e)}

async def fetch_air_quality(session, city):
    params = {
        "latitude":  city["lat"],
        "longitude": city["lon"],
        "current":   "pm2_5,pm10,us_aqi",
    }
    try:
        async with session.get(AIR_URL, params=params, timeout=TIMEOUT) as r:
            r.raise_for_status()
            data = await r.json()
            return data["current"]
    except Exception as e:
        return {"error": str(e)}


async def fetch_city(session, city):
    weather, air = await asyncio.gather(
        fetch_weather(session, city),
        fetch_air_quality(session, city),
    )
    return {"city": city["name"], "weather": weather, "air": air}

async def main():
    print(f"\n  Weather + Air Quality Dashboard")
    print(f"  {datetime.now().strftime('%d %b %Y  %H:%M')}")
    print(f"  {'─' * 54}\n")

    start = time.time()

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[fetch_city(session, city) for city in CITIES]
        )

    elapsed = time.time() - start

    header = f"  {'City':<12} {'Temp':>5} {'Humidity':>9} {'Wind':>8} {'AQI':>5}  Status"
    print(header)
    print(f"  {'─' * 54}")

    for r in results:
        city = r["city"]
        w    = r["weather"]
        a    = r["air"]
        if "error" in w:
            print(f"  {city:<12}  ERROR: {w['error']}")
            continue

        temp     = w.get("temperature_2m", "?")
        humidity = w.get("relative_humidity_2m", "?")
        wind     = w.get("wind_speed_10m", "?")
        aqi      = a.get("us_aqi", "?") if "error" not in a else "?"

        if isinstance(aqi, (int, float)):
            if aqi <= 50:   status = "Good"
            elif aqi <= 100: status = "Moderate"
            elif aqi <= 150: status = "Unhealthy"
            else:            status = "Very unhealthy"
        else:
            status = "N/A"

        print(f"  {city:<12} {temp:>4}C  {humidity:>6}%  {wind:>5}km/h  {aqi:>4}  {status}")

    print(f"\n  Fetched {len(CITIES)} cities in {elapsed:.2f}s "
          f"(async — all requests ran in parallel)\n")


asyncio.run(main())