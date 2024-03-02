import requests
import yaml
import redis
import json
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
'''API CALL'''
def createResponse(cityName:str) -> str:
    url = 'http://api.openweathermap.org/data/2.5/forecast?' + 'q=' + cityName + '&appid=' + str(apiKey)

    data = None
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
    else:
        print('Error with query')

    if data:
        return json.dumps(data)
    else: 
        return 'No Data Available'

'''REDIS Registering Specific Stuff'''

def setRedisData(cityNames : list[str]) -> None:
    
    for city in cityNames:
        redisClient.delete(f'WeatherData:{city}') #We only want one instance for this example
        redisClient.json().set(f'WeatherData:{city}', '.', createResponse(city))
        '''I was debating between sadd with only weather data or set with WeatherData+city
        I went with the latter because I feel this is a good use case incase I want temporal data in the future its more organized '''

        

def getCityData(city:str) -> dict:  
    weatherInfo = json.loads(redisClient.json().get(f'WeatherData:{city}'))
    
    return weatherInfo.get('city')

def getTempatures(city:str) -> tuple[int,int]:
    weatherInfo = json.loads(redisClient.json().get(f'WeatherData:{city}'))
    tempMin = weatherInfo.get('list')[0].get('main').get('temp_min')
    tempMax = weatherInfo.get('list')[0].get('main').get('temp_max')
    print('Temps: Min: ', KelvinToDegrees(tempMin),', Max: ', KelvinToDegrees(tempMax))
    return [KelvinToDegrees(tempMin),KelvinToDegrees(tempMax)]

def KelvinToDegrees(kelvin : int) -> int:
    return int((kelvin - 273.15) * (9/5) + 32)

def getElevation(city:str) -> int:
    weatherInfo = json.loads(redisClient.json().get(f'WeatherData:{city}'))
    print(weatherInfo.get('list')[2].get('main').get('sea_level'))
    return int(weatherInfo.get('list')[2].get('main').get('sea_level'))

def plotTempatures(cityNames : list[str]) -> None:
    if len(cityNames) > 2:
        print("Only supports two cities for now...")
    else:
        xMarks = [1,3]
        xNames = ['Lows','Highs']
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
        plt.title('Tempatures for 2/27/2024')
        plt.legend(['Chicago','Philadelphia'],loc='center right')
        plt.show()

def plotElevations(cityNames : list[str]) -> None:
    if len(cityNames) > 2:
        print("Only supports two cities for now...")
    else:
        xMarks = [.5,2]
        xNames = ['Chicago','Philadelphia']
        plt.xticks(xMarks,xNames)
        tempatureData = []
        for city in cityNames:
            tempatureData.append(getElevation(city))
        bar1 = plt.bar(.5,tempatureData[0], align='center', alpha=0.5,color='skyblue')
        plt.bar_label(bar1)

        bar2 = plt.bar(2,tempatureData[1], align='center', alpha=0.5,color='skyblue')
        plt.bar_label(bar2)

        plt.xlim([0,2.5])
        plt.title('SeaLevel')
        plt.show()

def plotGeoMap(cityNames : list[str]) -> None:
    #Set Lat and Lon Coordinate List That We Are Going To Display on Our Map
    lat = []
    lon = []

    for city in cityNames:
        cityData=getCityData(city)
        lat.append(int(cityData.get('coord').get('lat')))
        lon.append(int(cityData.get('coord').get('lon')))

    #set map and plot points
    map = Basemap()
    map.drawcoastlines()
    map.drawcountries()
    map.plot(lon,lat,'co',markersize=8) #make points cyan co
    #set city labels
    for i in range(0,len(cityNames)):
        plt.text(lon[i],lat[i] +2,cityNames[i][0:5],color='blue') #Grabs first 5 Letters and Plots them Accordingly
    plt.title("Cities")
    plt.show()

if __name__ == '__main__':
    #Pulling config data from yaml
    try:
        with open('../config.yaml', 'r') as config:
            data = yaml.safe_load(config)
    except:
        print('Error pulling data from config.yaml, Make sure your config.yaml is in the top directory and you cd into RedisInterface Folder')

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
    setRedisData(["Philadelphia","Chicago","Los Angeles"])
    #GET Functions for Data From REDIS
    getCityData('Philadelphia')
    getCityData('Chicago')
    getTempatures('Philadelphia')
    getTempatures('Chicago')
    getElevation('Philadelphia')
    getElevation('Chicago')

    #Plot City Comparisons
    citiesForComparisons = ['Chicago','Philadelphia']
    plotTempatures(citiesForComparisons)
    plotElevations(citiesForComparisons)
    plotGeoMap(["Philadelphia","Los Angeles"]) #Just these 2 for now because overlap isn't pretty.