import yaml
from OpenWeatherAPI import OpenWeatherAPI
from PlotHandler import PlotHandler
from RedisCommunications import RedisCommunications
if __name__ == '__main__':
    #Pulling config data from yaml
    try:
        with open('../config.yaml', 'r') as config:
            data = yaml.safe_load(config)
    except:
        print('Error pulling data from config.yaml, Make sure your config.yaml is in the top directory and you cd into RedisInterface Folder')

    openWeather =  OpenWeatherAPI(data)
    redisComms = RedisCommunications(openWeather,data)
    #Extract JSON from Weather API & Send it to Redis DB
    redisComms.setRedisData(["Philadelphia","Chicago","Los Angeles"])
    #GET Functions for Data From REDIS
    redisComms.getCityData('Philadelphia')
    redisComms.getCityData('Chicago')
    redisComms.getTempatures('Philadelphia')
    redisComms.getTempatures('Chicago')
    redisComms.getElevation('Philadelphia')
    redisComms.getElevation('Chicago')

    #Plot City Comparisons
    plotHandler = PlotHandler(redisComms)
    citiesForComparisons = ['Chicago','Philadelphia']
    plotHandler.plotTempatures(citiesForComparisons)
    plotHandler.plotElevations(citiesForComparisons)
    plotHandler.plotGeoMap(["Philadelphia","Los Angeles"]) #Just these 2 for now because overlap isn't pretty.