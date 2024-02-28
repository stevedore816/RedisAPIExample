import requests
import yaml

'''yaml related stuff'''

try:
    with open('../config.yaml', 'r') as config:
        data = yaml.safe_load(config)

    print("Host:", data['redis']['host'])
except:
    print("Error pulling data from config.yaml Make sure your in the top directory and following the template appropriately")

'''API CALL'''
api_key = data['OpenWeatherMapAPI']['api_key']
city_name = "Philadelphia"
url = "http://api.openweathermap.org/data/2.5/forecast?" + "q=" + city_name + "&appid=" + str(api_key)

response = requests.get(url)
print(response)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error with query")


'''REDIS Registering Specific Stuff'''