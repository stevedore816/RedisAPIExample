import requests
import yaml
import redis
import json
import matplotlib.pyplot as plt

'''API CALL'''
def createResponse(cityName:str):
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

def setRedisData(cityNames = ["Chicago","Philadelphia"]) :
    
    for city in cityNames:
        redisClient.delete(f'WeatherData:{city}') #We only want one instance for this example
        redisClient.json().set(f'WeatherData:{city}', '.', createResponse(city))
        '''I was debating between sadd with only weather data or set with WeatherData+city
        I went with the latter because I feel this is a good use case incase I want temporal data in the future its more organized '''

        

def getCityData(city:str):  
    weatherInfo = json.loads(redisClient.json().get(f'WeatherData:{city}'))
    
    print(weatherInfo.get('city'))

def getTempatures(city:str):
    weatherInfo = json.loads(redisClient.json().get(f'WeatherData:{city}'))
    tempMin = weatherInfo.get('list')[0].get('main').get('temp_min')
    tempMax = weatherInfo.get('list')[0].get('main').get('temp_max')
    print("Temps: Min: ", KelvinToDegrees(tempMin),", Max: ", KelvinToDegrees(tempMax))
    return [KelvinToDegrees(tempMin),KelvinToDegrees(tempMax)]

def KelvinToDegrees(kelvin : int) -> int:
    return int((kelvin - 273.15) * (9/5) + 32)

def getElevation(city:str):
    weatherInfo = json.loads(redisClient.json().get(f'WeatherData:{city}'))
    print(weatherInfo.get('list')[2].get('main').get('sea_level'))
    return weatherInfo.get('list')[2].get('main').get('sea_level')

def plotTempatures(cityNames = ["Chicago","Philadelphia"]) -> None:
    xMarks = [1,3]
    xNames = ["Lows","Highs"]
    plt.xticks(xMarks,xNames)
    tempatureData = []
    for city in cityNames:
        tempatureData.append(getTempatures(city))
    bar1 = plt.bar(.5,tempatureData[0][0], align='center', alpha=0.5,color='skyblue')
    plt.bar_label(bar1)

    bar2 = plt.bar(1.3,tempatureData[1][0], align='center', alpha=0.5,color='salmon')
    plt.bar_label(bar2)

    bar1 = plt.bar(2.5,tempatureData[0][1], align='center', alpha=0.5,color='skyblue')
    plt.bar_label(bar1)

    bar2 = plt.bar(3.3,tempatureData[1][1], align='center', alpha=0.5,color='salmon')
    plt.bar_label(bar2)

    plt.xlim([0,4])
    plt.title("Tempatures for 2/27/2024")
    plt.legend(["Chicago","Philadelphia"],loc='center right')
    plt.show()

def plotElevations(cityNames = ["Chicago","Philadelphia"]) -> None:
    xMarks = [.5,2]
    xNames = ["Chicago","Philadelphia"]
    plt.xticks(xMarks,xNames)
    tempatureData = []
    for city in cityNames:
        tempatureData.append(getElevation(city))
    bar1 = plt.bar(.5,tempatureData[0], align='center', alpha=0.5,color='skyblue')
    plt.bar_label(bar1)

    bar2 = plt.bar(2,tempatureData[1], align='center', alpha=0.5,color='skyblue')
    plt.bar_label(bar2)

    plt.xlim([0,2.5])
    plt.title("SeaLevel")
    plt.show()

if __name__ == '__main__':
    #Pulling config data from yaml
    try:
        with open('../config.yaml', 'r') as config:
            data = yaml.safe_load(config)
    except:
        print("Error pulling data from config.yaml Make sure your in the top directory and following the template appropriately")

    apiKey = data['OpenWeatherMapAPI']['api_key']
    
    #Instantiating Redis Client
    redisClient = redis.Redis(
    host = data['redis']['host'], 
    port=data['redis']['port'],
    db=data['redis']['db'],
    username=data['redis']['user'],
    password=data['redis']['password']
    )
    
    #Extract JSON from Weather API & Send it to Redis DB
    setRedisData()
    #GET Functions for Data From REDIS
    getCityData("Philadelphia")
    getCityData("Chicago")
    getTempatures("Philadelphia")
    getTempatures("Chicago")
    getElevation("Philadelphia")
    getElevation("Chicago")

    #Plot City Comparisons
    #plotTempatures()
    #plotElevations()