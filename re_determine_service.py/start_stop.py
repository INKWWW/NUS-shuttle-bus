#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

######## Detect the start or stop of service #########
## 1.I set the rest time at least 2 min = 120 s

### import
from openpyxl import load_workbook   #pip install openpyxl
from collections import namedtuple
import csv
import myfunction
import math

start_point = ['Prince George\'s Park Terminal', 'Kent Ridge Bus Terminal', 'Car Park 11', 'Car Park 11 (BIZ)', 'Botanic Gardens MRT']
stop_point = ['Prince George\'s Park Terminal', 'Kent Ridge Bus Terminal', 'Car Park 11', 'Car Park 11 (BIZ)', 'BTC - Oei Tiong Ham Building']
headers = ['gps_time', 'node_id','vehicle_serial','latitude', 'longitude', 'altitude', 'speed', 'heading', 'POI', 'start_stop', 'service']

with open('fenced_vehicle/2102_inside-2017-09-04.csv', 'r') as f_ss:  #with打开不用在意close
    r_ss = csv.reader(f_ss)
    headings_ss = next(r_ss)
    headings_ss.pop()
    headings_ss.pop()
    print(headings_ss)             
    SS = namedtuple('SS', headings_ss)   #用namedtuple 方便后面用headings来读取数据

    counter = 0

    with open('ss_vehicle/ss_2102_inside-2017-09-04.csv', 'w', newline ='') as fnew:    #use 'w' for writing str and newline='' for deleting extra idle row
        w_ss = csv.writer(fnew)
        w_ss.writerow(headers)
        for row_ss in r_ss:
            ss = SS._make(row_ss)
            counter += 1

            ### normal ###
            if (ss.POI not in start_point and ss.POI not in stop_point) :
                w_ss.writerow([row_ss[0], row_ss[1], row_ss[2], row_ss[3],row_ss[4], row_ss[5], row_ss[6], \
                        row_ss[7], row_ss[8]])
                counter = 0
                
            ### Stop ###
            #if there are only several POI in depot, I don't set its' location in depot
            if (ss.POI in start_point or ss.POI in stop_point) and (counter < 20):
                w_ss.writerow([row_ss[0], row_ss[1], row_ss[2], row_ss[3],row_ss[4], row_ss[5], row_ss[6], \
                        row_ss[7], row_ss[8]])

            # if (ss.POI in start_point or ss.POI in stop_point) and (20 <= counter <= 25):
            #     row_ss.append('stop')
            #     w_ss.writerow([row_ss[0], row_ss[1], row_ss[2], row_ss[3],row_ss[4], row_ss[5], row_ss[6], \
            #             row_ss[7], row_ss[8], row_ss[9]])

            if  (ss.POI in start_point or ss.POI in stop_point) and (counter >= 20) and (int(ss.speed) < 15):
                row_ss.append('stop')
                w_ss.writerow([row_ss[0], row_ss[1], row_ss[2], row_ss[3],row_ss[4], row_ss[5], row_ss[6], \
                        row_ss[7], row_ss[8], row_ss[9]])

            ### Start ###
            if (ss.POI in start_point or ss.POI in stop_point) and (counter >= 20) and (int(ss.speed) >= 15):
                row_ss.append('start')
                w_ss.writerow([row_ss[0], row_ss[1], row_ss[2], row_ss[3],row_ss[4], row_ss[5], row_ss[6], \
                        row_ss[7], row_ss[8], row_ss[9]])
                

                