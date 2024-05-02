from django.shortcuts import render
# import json to losd json data to python directory
import json
# urllib.request to make a request to api
import urllib.request

# to load the api key
import os
from dotenv import load_dotenv

# load env vairable from .env file
load_dotenv()

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        # getting api key
        api_key = os.getenv("API_KEY")
        # source contain JSON data from API

        source = urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+ city + ',' + state + ',' + country + '&limit=5&appid=' + api_key).read()
        
        # converting JSON data to a dictionary
        list_of_data = json.loads(source)

        # data for variable list_of_data
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon'] + ' ' + str(list_of_data['coord']['lat'])),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['humidity']),
        }
        print(data)
    else:
        data = {}

    return render(request, 'main/index.html', data)