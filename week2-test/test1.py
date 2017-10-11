#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

#determine the vehicle's start of service

from collections import namedtuple
import csv

vehicleid = input('please input the vehicleid: ')  
headers = ['gps_time', 'node_id','vehicle_serial','latitude', 'longitude', 'altitude', 'speed', 'heading']
counter_stop = 0

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
            vehicle = Vehicle._make(row_v)
            if vehicle.node_id == vehicleid:
                #将时间 +8 转换到Singapore时区
                time = vehicle.gps_time
                date_time = int(time.split('T')[0].split('-')[2])
                hour_time = int(time.split('T')[1].split(':')[0])
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

                #estimate the start of service
                if (int(vehicle.speed) == 0) or (int(vehicle.speed) == 1):    #注意int()转换后进行比较！！！读取出来是string！！！
                    counter_stop += 1
                if (int(vehicle.speed) > 1) and (counter_stop <= 65):  #！注意条件判断：两个if内的数字必须要是一样的，无缝判断。要不会漏了中间的数据！
                    counter_stop = 0
                if (int(vehicle.speed) > 1) and (counter_stop > 65):     #注意判断的条件 or/and， 用什么条件来判断！还有就是if的嵌套关系！！
                    counter_stop = 0
                    w_vehicle.writerow([' '])
                    w_vehicle.writerow(['start of service'])
                    w_vehicle.writerow([' '])










                










