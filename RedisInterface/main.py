import requests
import yaml
import redis
import json
'''yaml related stuff'''

try:
    with open('../config.yaml', 'r') as config:
        data = yaml.safe_load(config)

    print("Host:", data['redis']['host'])
except:
    print("Error pulling data from config.yaml Make sure your in the top directory and following the template appropriately")

'''API CALL'''


apiKey = data['OpenWeatherMapAPI']['api_key']
def createResponse():
    cityName = "Philadelphia"
    url = "http://api.openweathermap.org/data/2.5/forecast?" + "q=" + cityName + "&appid=" + str(apiKey)

    data = None
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
    else:
        print("Error with query")

    if data:
        return json.dumps(data)
    else: 
        return "No Data Available"

'''REDIS Registering Specific Stuff'''

redisClient = redis.Redis(
    host = data['redis']['host'], 
    port=data['redis']['port'],
    db=data['redis']['db'],
    username=data['redis']['user'],
    password=data['redis']['password'],
    ssl=False
)


redisClient.delete('jsonData')

redisClient.set('WeatherData', createResponse())

print(redisClient.get('WeatherData'))


