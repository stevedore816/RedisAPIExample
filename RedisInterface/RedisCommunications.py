import redis
import OpenWeatherAPI
import json
class RedisCommunications:
    def __init__(self,weatherAPI: OpenWeatherAPI,yamlData) -> None:
        self.weatherAPI= weatherAPI
        #Instantiating Redis Client
        self.redisClient = redis.Redis(
        host = yamlData['redis']['host'], 
        port=yamlData['redis']['port'],
        db=yamlData['redis']['db'],
        username=yamlData['redis']['user'],
        password=yamlData['redis']['password']
        )
    def setRedisData(self,cityNames : list[str]) -> None:
        """    
        Sends the city data from the OpenWeatherAPI over to Redis via RedisJSON

        Args:
            cityNames: List of Cities that we want to store in Redis

        Returns:
            None
        """
        
        for city in cityNames:
            self.redisClient.delete(f'WeatherData:{city}') #We only want one instance for this example
            self.redisClient.json().set(f'WeatherData:{city}', '.', self.weatherAPI.createResponse(city))
        '''I was debating between sadd with only weather data or set with WeatherData+city
        I went with the latter because I feel this is a good use case incase I want temporal data in the future its more organized '''

        

    def getCityData(self,cityName:str) -> dict:  
        """    
            Searches in REDIS for a city that we then traverse to get information about the city itself. 

        Args:
            cityName: Name of the City we want to query. 

        Returns:
            A Dictionary Containing the City Data in REDIS
        """
        weatherInfo = json.loads(self.redisClient.json().get(f'WeatherData:{cityName}'))
        
        return weatherInfo.get('city')

    def getTempatures(self,cityName:str) -> tuple[int,int]:
        """    
            Searches in REDIS for a city that we then traverse to get information about the tempatures.

        Args:
            cityName: Name of the City we want to query. 

        Returns:
            A Tuple Containing the Low and High tempatures for the city. 
        """
        weatherInfo = json.loads(self.redisClient.json().get(f'WeatherData:{cityName}'))
        tempMin = weatherInfo.get('list')[0].get('main').get('temp_min')
        tempMax = weatherInfo.get('list')[0].get('main').get('temp_max')
        print('Temps: Min: ', self.KelvinToDegrees(tempMin),', Max: ', self.KelvinToDegrees(tempMax))
        return [self.KelvinToDegrees(tempMin),self.KelvinToDegrees(tempMax)]

    def KelvinToDegrees(self,kelvin : int) -> int:
        """    
        Converts from Kelvin to Degrees

        Args:
        kelvin: the tempature to be converted to degrees

        Returns:
        The conversion of kelvin tempature in Degrees
        """
        return int((kelvin - 273.15) * (9/5) + 32)

    def getElevation(self,cityName:str) -> int:
        """    
        Searches in REDIS for a city that we then traverse to get information about the sealevel.

        Args:
        cityName: Name of the City we want to query. 

        Returns:
        An int indicating how high above sealevel the respective city is 
        """
        weatherInfo = json.loads(self.redisClient.json().get(f'WeatherData:{cityName}'))
        print(weatherInfo.get('list')[2].get('main').get('sea_level'))
        return int(weatherInfo.get('list')[2].get('main').get('sea_level'))