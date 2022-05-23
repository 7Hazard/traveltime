import shapefile as shp
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point, Polygon

sf = shp.Reader("data/zones/taxi_zones.shp")

plt.figure()
for shape in sf.shapeRecords():
    for i in range(len(shape.shape.parts)):
        i_start = shape.shape.parts[i]
        if i==len(shape.shape.parts)-1:
            i_end = len(shape.shape.points)
        else:
            i_end = shape.shape.parts[i+1]
        x = [i[0] for i in shape.shape.points[i_start:i_end]]
        y = [i[1] for i in shape.shape.points[i_start:i_end]]
        plt.plot(x,y)
        # print shape metadata
        # print(shape.record)
        # print shape zone code
        zoneCode = shape.record[0]
        print(zoneCode)
plt.show()

def latlonToZone(lon, lat):
    point = Point(lon, lat)
    for sr in sf.shapeRecords():
        sr: shp.ShapeRecord
        shape: shp.Shape = sr.shape
        polygon = Polygon(shape.points)
        print(polygon)
        if polygon.within(point):
            return sr.record[0]
    return None

print(latlonToZone(40.7128, -74.0060))
