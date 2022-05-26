import shapefile as shp
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import pandas as pd

# Dataset name:	taxi_zones
# Format:	ESRI Shapefile (shp)
# File size:	1737443 bytes
# Layers count:	1
# Dataset extent:
# Min X: 913175.109008804
# Min Y: 120121.88125434518
# Max X: 1067382.508405164
# Max Y: 272844.2940054685
# Extent WGS 84 (lat/lon):
# Min X: -74.25554696612534
# Min Y: 40.496096946233486
# Max X: -73.69921518371616
# Max Y: 40.915175851595436
# Coordinate system: +proj=lcc +lat_1=40.66666666666666 +lat_2=41.03333333333333 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000 +y_0=0 +datum=NAD83 +units=us-ft +no_defs
# sf = shp.Reader("data/zones/taxi_zones.shp")

__sf = shp.Reader("data/zones/taxi_zones.zip")

def plotZones():
    plt.figure()
    for shape in __sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(x,y)
    plt.show()

def latlonToZoneId(lon, lat):
    x, y = lon, lat
    point = Point(x, y)

    # find the zone that contains the point
    for sr in __sf.shapeRecords():
        sr: shp.ShapeRecord
        shape: shp.Shape = sr.shape
        polygon = Polygon(shape.points)
        if polygon.contains(point):
            return sr.record[0]

    return None

# plotZones()
# print(latlonToZoneId(-74.012130, 40.692293))

# read all taxi zones from csv file
__taxi_zones = pd.read_csv("data/zones/taxi_zone_lookup.csv")

# print string Zone of zone LocationID 105
# print(__taxi_zones[__taxi_zones.LocationID == 105]["Zone"].values[0])

def zoneIdToName(id):
    return __taxi_zones[__taxi_zones.LocationID == id]["Zone"].values[0]

# print 10 random rows from taxi_zones
# print(__taxi_zones.head(110))

# print(zoneIdToName(latlonToZoneId(-74.012130, 40.692293)))



