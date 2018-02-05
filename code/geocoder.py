import pandas as pd
import numpy as np
from shapely.geometry import Point
import geopandas as gpd
import pyproj
from shapely.geometry import Polygon, MultiPolygon,Point, MultiPoint
from shapely.ops import nearest_points
import geocoder

def convert_poly(polygon):
    #convert New York State coordinates to Longitude and Latitude
    NYSP1983 = pyproj.Proj(init="ESRI:102718", preserve_units=True)
    gis = []
    for coo in list(polygon.exterior.coords):
        x,y = coo
        gis.append(NYSP1983(x, y, inverse=True))
    return Polygon(gis)

def convert_multi(multi):
    if isinstance(multi, MultiPolygon):
        out = []
        for poly in multi.geoms:
            out.append(convert_poly(poly))
        return MultiPolygon(out)
    else:
        return convert_poly(multi)

def nearest(row, geom_union, df1, df2, geom1_col='geometry', geom2_col='geometry', src_column=None):
    #Find the nearest point and return the corresponding value from specified column.
    nearest = df2[geom2_col] == nearest_points(row[geom1_col], geom_union)[1]
    value = df2[nearest][src_column].get_values()[0]
    return value

def geocode(key, add_list, offset, chunk=2500):
    #geocode address
    location = []
    for i in range(offset, offset+chunk):
        try:
            x = add_list[i]
        except IndexError as e:
            raise e
        geo = geocoder.arcgis(x)
        time.sleep(0.1)
        if geo.ok:
            location.append(geo.latlng)
            del geo
        elif geo.status == 'ERROR - No results found':
            geo = geocoder.google(x, key=key)
            if geo.ok:
                print('google')
                location.append(geo.latlng)
                del geo
            else:
                print(x)
                print(geo.status)
                break            
        else:
            print(x)
            print(geo.status)
            break
        if (i%1000) == 0:
            print(i)
            np.save('data/location.npy', location)


if __name__ == '__main__':
    print('geocoder')