#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

from collections import namedtuple
import csv

vehicleid = input('please input the vehicleid: ')  
headers1 = ['gps_time', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
headers2 = ['session_id', 'mac_hash', 'ts_time']
headers = ['gps_time', 'latitude', 'longitude', 'altitude', 'speed', 'heading', 'session_id', 'mac_hash','ts_time']
counter1 = -1
counter2 = -1

#read the data from vehicle and create a file to save data
with open('../Veniam_BusLocation/2017_week35/2017-08-28.csv', 'r') as f_vehicle_r: #with打开不用在意close
    f_vehicle = csv.reader(f_vehicle_r)
    headings_v = next(f_vehicle)              
    Row_vehicle = namedtuple('Row_vehicle', headings_v)   #给namedtuple 方面后面用headings来读取数据
    with open('newcsvfile.csv', 'w') as f_vehicle_w:
        fv_writer = csv.writer(f_vehicle_w)
        #fv_writer.writerow(headers1)
        for r_v in f_vehicle:
            row_v = Row_vehicle(*r_v)
            if row_v.node_id == vehicleid:
                fv_writer.writerow([r_v[2],r_v[3],r_v[4],r_v[5],r_v[6],r_v[7]])
#   f_vehicle_w.close()
# f_vehicle_r.close()

#read the data from the devices and create a file to save data
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
#   f_device_w.close()
# f_device_r.close()

#compare these two files to get the correlative data
with open('newcsvfile.csv', 'r') as vinfo, open('newcsvfile2.csv', 'r') as dinfo:
    vinforeader = csv.reader(vinfo)
    dinforeader = csv.reader(dinfo)
    newfilename = '_'.join([vehicleid, '2017-08-28.csv'])  #根据不同的车辆号码输入创建不同的文件名
    with open(newfilename, 'w') as fnew:
        fnew_writer = csv.writer(fnew)
        fnew_writer.writerow(headers)
        vlist = vinfo.readlines()    #readlines可以以及读取所有内容并且按行返回list，内容为string
        dlist = dinfo.readlines()
        for n in vlist:
            counter1 = counter1 + 1
            v_time = str(n).split(',')[0].strip()   #提取出vehicle的时间，一定记得strip()掉字符串前后的空格，为了比较
            fnew_writer.writerow([ str(n).split(',')[0], str(n).split(',')[1], str(n).split(',')[2], str(n).split(',')[3],\
                        str(n).split(',')[4], str(n).split(',')[5]])
            for m in dlist:
                counter2 = counter2 + 1
                d_time = str(m).split(',')[2].strip()
                if v_time == d_time:
                    # print(v_time)
                    # print('success')
                    # print(d_time)
                    # print('okokok')
                    result = n.strip() + m
                    print(result)
                    fnew_writer.writerow([ str(n).split(',')[0], str(n).split(',')[1], str(n).split(',')[2], str(n).split(',')[3],\
                        str(n).split(',')[4], str(n).split(',')[5], str(m).split(',')[0], str(m).split(',')[1], str(m).split(',')[2] ])

    # print(type(v_time))
    # print(type(d_time))
    print('Done!')
