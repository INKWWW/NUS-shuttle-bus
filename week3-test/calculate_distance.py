#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

#calculate the distance if I know the altitude and longitude, unit:M

from math import radians, cos, sin, asin, sqrt

def cal_dis(poi_latitude, poi_longitude, vehicle_latitude, vehicle_longitude):
    #invert the degree number to radian
    poi_latitude, poi_longitude, vehicle_latitude, vehicle_longitude = \
    map(radians, [poi_latitude, poi_longitude, vehicle_latitude, vehicle_longitude])

    #calculate the distance
    dis_latitude = vehicle_latitude - poi_latitude
    dis_longitude = vehicle_longitude - poi_longitude
    a = sin(dis_longitude / 2) ** 2 + cos(poi_longitude) * cos(vehicle_longitude) * \
    sin(dis_latitude / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371 # the radius of the earth, unit: KM
    dis = c * r * 1000
    return dis
