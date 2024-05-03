from django.shortcuts import render
import json
import urllib.request
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        api_key = os.getenv("API_KEY")
        # Fetch weather data using the correct API endpoint
        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' 
            + city + '&appid=' + api_key).read()
        
        # Convert JSON data to a dictionary
        weather_data = json.loads(source)

        # Extract required weather information
        if 'main' in weather_data:
            country_code = weather_data['sys']['country']
            coordinate = f"{weather_data['coord']['lon']} {weather_data['coord']['lat']}"
            temp = f"{round(weather_data['main']['temp']-273.15, 2)}C"
            pressure = weather_data['main']['pressure']
            humidity = f"{weather_data['main']['humidity']}%"

            # ranging atmospheric pressure 
            if pressure >= 1050:
                pres = "High Pressure"
            elif pressure <= 29.80:
                pres = "Low Pressure"
            else:
                pres = "Normal"

            
            # Prepare data to pass to the template
            data = {
                "city": city,
                "country_code": country_code,
                "coordinate": coordinate,
                "temp": temp,
                "pressure": pres,
                "humidity": humidity,
            }
        else:
            # If weather data is not available for the given city
            data = {"error": "Weather data not found for the provided city."}
    else:
        data = {}

    return render(request, 'main/index.html', data)
