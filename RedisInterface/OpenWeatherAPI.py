import json
import requests
class OpenWeatherAPI:
    """
    This class handles communicating with OpenWeatherAPI to Pull data
    Attributes:
        apikey: key for querying data
    """
    def __init__(self,yamlData) -> None:
        """
        Initalize the OpenWeatherAPI Class

        Args:
            yamlData: Data from the yaml file to instantiate Redis Client
        """
        self.apiKey = yamlData['OpenWeatherMapAPI']['api_key']

    def createResponse(self,cityName:str) -> str:
        """    
        Sends API Request to OpenWeatherAPI

        Args:
            cityName: Name of the City we want to query. 

        Returns:
            A JSON String of all the Weather Data at the moment from OpenWeatherAPI
        """
        url = 'http://api.openweathermap.org/data/2.5/forecast?' + 'q=' + cityName + '&appid=' + str(self.apiKey)

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
