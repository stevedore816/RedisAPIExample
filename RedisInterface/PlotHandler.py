import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import RedisCommunications
class PlotHandler():
    def __init__(self,RedisClient:RedisCommunications) -> None:
        self.redisClient=RedisClient
    def plotTempatures(self,cityNames : list[str]) -> None:
        """    
        Plots a comparision of 2 Cities Tempatures

        Args:
            cityNames:  List of Cities we want to compare (Can only be 2)

        Returns:
            None
        """
        if len(cityNames) > 2:
            print("Only supports two cities for now...")
        else:
            xMarks = [1,3]
            xNames = ['Lows','Highs']
            plt.xticks(xMarks,xNames)
            tempatureData = []
            for city in cityNames:
                tempatureData.append(self.redisClient.getTempatures(city))
            bar1 = plt.bar(.5,tempatureData[0][0], align='center', alpha=0.5,color='skyblue')
            plt.bar_label(bar1)

            bar2 = plt.bar(1.3,tempatureData[1][0], align='center', alpha=0.5,color='salmon')
            plt.bar_label(bar2)

            bar1 = plt.bar(2.5,tempatureData[0][1], align='center', alpha=0.5,color='skyblue')
            plt.bar_label(bar1)

            bar2 = plt.bar(3.3,tempatureData[1][1], align='center', alpha=0.5,color='salmon')
            plt.bar_label(bar2)

            plt.xlim([0,4])
            plt.title('Tempatures for 3/01/2024')
            plt.legend(['Chicago','Philadelphia'],loc='center right')
            plt.show()

    def plotElevations(self,cityNames : list[str]) -> None:
        """    
        Plots a comparision of 2 Cities Elevations

        Args:
            cityNames:  List of Cities we want to compare (Can only be 2)

        Returns:
            None
        """
        if len(cityNames) > 2:
            print("Only supports two cities for now...")
        else:
            xMarks = [.5,2]
            xNames = ['Chicago','Philadelphia']
            plt.xticks(xMarks,xNames)
            tempatureData = []
            for city in cityNames:
                tempatureData.append(self.redisClient.getElevation(city))
            bar1 = plt.bar(.5,tempatureData[0], align='center', alpha=0.5,color='skyblue')
            plt.bar_label(bar1)

            bar2 = plt.bar(2,tempatureData[1], align='center', alpha=0.5,color='skyblue')
            plt.bar_label(bar2)

            plt.xlim([0,2.5])
            plt.title('SeaLevel')
            plt.show()

    def plotGeoMap(self,cityNames : list[str]) -> None:
        """    
        Plots city locations on a map

        Args:
            cityNames:  List of Cities we want to visualize

        Returns:
            None
        """
        #Set Lat and Lon Coordinate List That We Are Going To Display on Our Map
        lat = []
        lon = []

        for city in cityNames:
            cityData=self.redisClient.getCityData(city)
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
