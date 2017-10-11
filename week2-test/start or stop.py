#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

from collections import namedtuple
import csv

vehicleid = input('please input the vehicleid: ')  
headers = ['gps_time', 'node_id','session_id','latitude', 'longitude', 'altitude', 'speed', 'heading']

#read the data from vehicle and create a file to save data
with open('../Veniam_BusLocation/2017_week35/2017-08-28.csv', 'r') as f_vehicle:  #with打开不用在意close
    r_vehicle = csv.reader(f_vehicle)
    headings_v = next(r_vehicle)
    # print(headings_v)              
    Vehicle = namedtuple('Vehicle', headings_v)   #给namedtuple 方面后面用headings来读取数据
    newfilename = '_'.join([vehicleid, '2017-08-28.csv'])  #根据不同的车辆号码输入创建不同的文件名
    with open(newfilename, 'w') as fnew:
        w_vehicle = csv.writer(fnew)
        w_vehicle.writerow(headers)
        for row_v in r_vehicle:
            vehicle = Vehicle._make(row_v)   #因为row_v是字符串，所以要用 ._make方法
            if vehicle.node_id == vehicleid:
                time = vehicle.gps_time
                # print(time)
                date_time = int(time.split('T')[0].split('-')[2])
                hour_time = int(time.split('T')[1].split(':')[0])
                # print(hour_time)
                minsec_time = time.split(':')[1] + ':' + time.split(':')[2]
                if (date_time + 1) == 28:
                    date_time = date_time + 1
                else:
                    date_time = date_time

                if (hour_time + 8) > 24:
                    hour_time = hour_time + 8 - 24 
                else:
                    hour_time = hour_time + 8

                new_time = time.split('T')[0].split('-')[0] + '-' + time.split('T')[0].split('-')[1] + '-' + str(date_time) + 'T' \
                    + ' ' + str(hour_time) + ':' + minsec_time
                w_vehicle.writerow([new_time, row_v[0],row_v[1],row_v[3],row_v[4],row_v[5],row_v[6],row_v[7]])


    