#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

from collections import namedtuple
import csv

with open('../Veniam_BusLocation/2017_week43/2017-10-23.csv', 'r') as f_vehicle:  #with打开不用在意close
    r_vehicle = csv.reader(f_vehicle)
    headings_v = next(r_vehicle)
    # print(headings_v)              
    Vehicle = namedtuple('Vehicle', headings_v)   #用namedtuple 方便后面用headings来读取数据
    nodeid_list = []
    nodeid_counter = 0
    for row_v in r_vehicle:
        vehicle = Vehicle._make(row_v)
        if vehicle.node_id not in nodeid_list:
            nodeid_list.append(vehicle.node_id)
            nodeid_counter = nodeid_counter + 1

print(nodeid_counter)
print(nodeid_list)