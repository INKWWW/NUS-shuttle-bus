#!/usr/bin/python
# -*-coding: UTF-8-*-

#按照column读取
    # for index, rows in enumerate (f_csv):
    #   if index == 1:
    #       row = rows
    # print (row)

from collections import namedtuple 
import csv

vehicleid = input('please input the vehicleid: ')  
headers1 = ['gps_time', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
headers2 = ['session_id', 'mac_hash', 'ts_time']
headers = ['gps_time', 'latitude', 'longitude', 'altitude', 'speed', 'heading', 'session_id', 'mac_hash','ts_time']
counter1 = -1
counter2 = -1

#read the data from vehicle
with open('../Veniam_BusLocation/2017_week35/2017-08-28.csv', 'r') as f_vehicle_r:
    f_vehicle = csv.reader(f_vehicle_r)
    headings_v = next(f_vehicle)
    Row_vehicle = namedtuple('Row_vehicle', headings_v)  #namedtuple让row读取的时候可以带上属性，更明确

    with open('newcsvfile.csv', 'w') as f_vehicle_w:
        fv_writer = csv.writer(f_vehicle_w)
        fv_writer.writerow(headers1)
        for r_v in f_vehicle:
            row_v = Row_vehicle(*r_v)
            if row_v.node_id == vehicleid:
                # print(r_v[0],r_v[1])
                fv_writer.writerow([r_v[2],r_v[3],r_v[4],r_v[5],r_v[6],r_v[7]])
    f_vehicle_w.close()
f_vehicle_r.close()

#read the data from the devices
with open('../Veniam_Session/2017_week35/2017-08-28.csv', 'r') as f_device_r:
    f_device = csv.reader(f_device_r)
    headings_d = next(f_device)
    Row_device = namedtuple('Row_device', headings_d) 

    with open('newcsvfile2.csv', 'w') as f_device_w:
        fd_writer = csv.writer(f_device_w)
        fd_writer.writerow(headers2)
        for r_d in f_device:
            row_d = Row_device(*r_d)
            if row_d.gw_id == vehicleid:                
                fd_writer.writerow([r_d[0], r_d[1], r_d[3]])
    f_device_w.close()
f_device_r.close()

with open('newcsvfile.csv', 'r') as vinfo, open('newcsvfile2.csv', 'r') as dinfo:
    vinforeader = csv.reader(vinfo)
    dinforeader = csv.reader(dinfo)
    with open('new3.csv', 'w') as fnew:
        fnew_writer = csv.writer(fnew)
        fnew_writer.writerow(headers)
        vlist = vinfo.readlines()
        dlist = dinfo.readlines()
        for n in vlist:
            counter1 = counter1 + 1
            v_time = str(n).split(',')[0].strip() #通过单独打印可以看出split之后会有空行（空格），这是之前导致if语句比对str不成功的原因。所以需要strip。
            for m in dlist:
                counter2 = counter2 + 1
                d_time = str(m).split(',')[2].strip()
                if v_time == d_time:
                    # print(v_time)
                    # print('success')
                    # print(d_time)
                    # print('okokok')
                    # print(str(n).split(',')[])
                    result = n.strip() + m
                    print(result)
                    fnew_writer.writerow([ str(n).split(',')[0], str(n).split(',')[1], str(n).split(',')[2], str(n).split(',')[3],\
                        str(n).split(',')[4], str(n).split(',')[5], str(m).split(',')[0], str(m).split(',')[1], str(m).split(',')[2] ])


                
    
    #尝试失败 哈哈哈哈
    # while vinfo.readline() != '':
    #   counter1 = counter1 + 1
    #   vlist = vinfo.readline()
    #   v_time = str(vlist).split(',')[0].strip()
    #   while dinfo.readline() != '':
    #       counter2 = counter2 + 1
    #       dlist = dinfo.readline()
    #       d_time = str(dlist).split(',')[2].strip()
    #       if v_time == d_time:
    #           print('success')
    #           final = vlist[counter1].append(dlist[counter2])



    print(type(v_time))
    print(type(d_time))






    




    
    















