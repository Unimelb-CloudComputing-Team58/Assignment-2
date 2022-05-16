from math import radians, cos, sin, asin, sqrt, pi
import json
import os
import json
import shapefile
from shapely.geometry import Point  # Point class
from shapely.geometry import shape  # shape() is a function to convert geo objects through the interface
from tqdm import tqdm
import pickle

shp = shapefile.Reader(
    r'C:\Users\thoma\Desktop\IT\CCC\A2\Assignment-2\aurin_data\shp_files\spatialise-SA4\shp\apm_sa4_2016_timeseries-.shp')  # open the shapefile
all_shapes = shp.shapes()  # get all the polygons
all_records = shp.records()


def count_coord(resp):
    count = 0
    for res in resp:
        if res._json['coordinates'] != None:
            count += 1
    return count


def save_json(resp, lat_gap, long_gap):
    if len(resp) != 0:
        file_path = "1km_gap_food/Recent_tweet_" + str(lat_gap) + "_" + str(long_gap) + ".json"
        with open(file_path, "a", encoding="utf-8") as fp:
            for res in resp:
                j = json.dumps(res._json)
                fp.write(j + '\n')


def save_log(counter, tweet_line, geo_count, lat_gap, long_gap):
    with open("1km_gap_food/log.log", "a", encoding="utf-8") as f:
        f.write(str(lat_gap) + "_" + str(long_gap) + '\n')
        log = "count: " + str(counter) + " tweet_line: " + str(tweet_line) + " Geo_count:" + str(geo_count)
        f.write(log + '\n')


def get_new_lat(lng1, lat1, dist=1000):
    """

    :param lng1: 116.498079
    :param lat1: 39.752304
    :param dist: Distance
    :return: (116.498079,39.756801)
    """
    # 6371 * 1000 为地球半径，单位米
    lat2 = 180 * dist / (6371 * 1000 * pi) + lat1
    return lat2


def get_new_lng(lng1, lat1, dist=1000):
    """

    :param lng1: 116.498079
    :param lat1: 39.752304
    :param dist: Distance
    :return: (116.503928,39.752304)
    """
    lng2 = 180 * dist / (6371 * 1000 * pi * cos(radians(lat1))) + lng1
    return lng2


if __name__ == "__main__":
    lat_center = -37.81585
    long_center = 144.96313
    gap = 1
    counter = 1
    tweet_line = 0
    geo_count = 0
    max_id = 0
    point_count = 0
    valid_coord = []
    valid_coord_dic = {}
    area_count = {}
    for lat_gap in tqdm(range(-150, 150, 10)):
        for long_gap in range(-150, 150, 10):
            new_lat = get_new_lat(long_center, lat_center, 1000 * lat_gap)
            new_lng = get_new_lng(long_center, lat_center, 1000 * long_gap)
            point_to_check = (new_lng, new_lat)
            for i in range(len(all_shapes)):
                boundary = all_shapes[i]  # get a boundary polygon
                if Point(point_to_check).within(shape(boundary)):
                    point_count += 1
                    valid_coord.append((new_lat, new_lng))
                    name = all_records[i][4]
                    if name not in valid_coord_dic:
                        valid_coord_dic[name] = []
                        valid_coord_dic[name].append((new_lat, new_lng))
                    else:
                        valid_coord_dic[name].append((new_lat, new_lng))
                    area_count[name] = area_count.get(name, 0) + 1

    dic_file = "area_coordinate.pkl"
    a_file = open(dic_file, "wb")
    pickle.dump(valid_coord_dic, a_file)
    a_file.close()

    a_file = open(dic_file, "rb")
    area_coordinate_dic = pickle.load(a_file)
    print(area_coordinate_dic)
    a_file.close()

    def bounding_box(long_center,lat_center,dist = 5000):
        east_lon = get_new_lng(long_center, lat_center, dist)
        west_lon = get_new_lng(long_center, lat_center, -dist)
        north_lat = get_new_lat(long_center, lat_center, dist)
        south_lat = get_new_lat(long_center, lat_center, -dist)
        print(west_lon, south_lat, east_lon, north_lat)
        bounding_box_string = "bounding_box:[" + str(west_lon) + ' ' + str(south_lat) + ' ' + str(east_lon) + ' ' + str(
            north_lat) + "]"
        return bounding_box_string