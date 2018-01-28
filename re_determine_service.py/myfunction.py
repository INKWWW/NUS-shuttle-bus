#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

#There are my functions 
import math
from math import radians, cos, sin, asin, sqrt

#################################################################################
#calculate the distance if I know the altitude and longitude, unit:M
def cal_distance(poi_latitude, poi_longitude, vehicle_latitude, vehicle_longitude):
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

##################################################################################
#calculate the slope of two arbitrary points，which is used to decide whether the vihicle is in the Depot
def cal_slope(a, b, x, y):
    slope = (b - y) / (a - x)
    return slope

######################################## Geo Fencing #########################################
# Improved point in polygon test which includes edge and vertex points
# This geo fence is NUS Area(Kent Ridge & Botanic), used to eliminate the location data outside NUS campus
def point_in_poly(x,y,poly):
   # check if point is a vertex
   if (x,y) in poly: 
      return "IN"
   # check if point is on a boundary
   for i in range(len(poly)):
      p1 = None
      p2 = None
      if i==0:
         p1 = poly[0]
         p2 = poly[1]
      else:
         p1 = poly[i-1]
         p2 = poly[i]
      if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
         return "IN"      
   n = len(poly)
   inside = False
   p1x,p1y = poly[0]
   for i in range(n+1):
      p2x,p2y = poly[i % n]
      if y > min(p1y,p2y):
         if y <= max(p1y,p2y):
            if x <= max(p1x,p2x):
               if p1y != p2y:
                  xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
               if p1x == p2x or x <= xints:
                  inside = not inside
      p1x,p1y = p2x,p2y

   if inside: 
      return "IN"
   else: 
      return "OUT"

#################################################################################
#ccompare two list(A, B):A > B; if A contains B's all the elements, output Ture; otherwise, output False
def list_compare(A, B):
    counter = 0
    for i in B:
      if i in A:
        counter = counter + 1
        # print(i)
      # else:
      #   counter -= 1
    print('A: ', len(A))
    print('A has --- ', A)
    print('B: ', len(B))
    print('B has --- ', B)
    print('counter: ', counter)
    if ( counter == len(B) ) or ( counter == len(B) - 1) :
      return True
    else:
      return False

#########Find all the vehicles' node_id in this day##########
#find all node_id and put them into a array

























