import json
import requests
class OpenWeatherAPI:

    def __init__(self,yamlData) -> None:
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
