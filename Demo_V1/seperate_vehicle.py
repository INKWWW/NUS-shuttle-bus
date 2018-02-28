#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

################################################# Sperate each vehicle ############################################
'''This step is to seperate every vehicle's data and write them into a separate CSV file

    Second step
'''

from openpyxl import load_workbook   #pip install openpyxl
from collections import namedtuple
import csv
import MyFunctions      
import pdb

def AllBusNodeid(filepath):
    '''Extract all vehicles running in a particular day - Get all node_id
        Filepath: 使用经过Geo Fence和计算并标记了POI的表的路径
    '''
    with open(filepath, 'r') as f_vehicle:  #with打开不用在意close
        r_vehicle = csv.reader(f_vehicle)
        # print(headings_v)              
        nodeid_list = []
        nodeid_license = {}
        nodeid_counter = 0
        header = next(r_vehicle)
        for row_v in r_vehicle:
            if row_v[0] not in nodeid_list:
                nodeid_list.append(row_v[0])
                nodeid_counter = nodeid_counter + 1
                nodeid_license[row_v[0]] = row_v[1]
        # print('all node_id today: ', nodeid_counter)
        print('node_id_list: ', nodeid_list)
        # print('nodeid_license: ', nodeid_license)
        return nodeid_list

def seperate_vehicle(filepath, nodeid_list):
    '''
       filepath: 使用经过Geo Fence和计算并标记了POI的表的路径 
    '''   
    headers = ['node_id', 'vehicle_serial', 'gps_time', 'latitude', 'longitude', 'altitude', 'speed', 'heading', 'POI']
    
    for vehicleid in nodeid_list:
        with open(filepath, 'r') as f_vehicle:  #with打开不用在意close
            r_vehicle = csv.reader(f_vehicle)
            headings_v = next(r_vehicle)
            # print(headings_v)              
            Vehicle = namedtuple('Vehicle', headings_v)   #用namedtuple 方便后面用headings来读取数据
            newfilename = '-'.join([vehicleid, filepath[14:] ])  #根据不同的车辆号码输入创建不同的文件名
            newpath = '/'.join(['fenced_vehicle', filepath[14:24], newfilename])
            print(newpath)
            MyFunctions.checkPath(newpath)  #checkPath 检查文件路径是否正确，不正确的话就进行创建
            with open(newpath, 'w', newline ='') as fnew:    #use 'w' for writing str and newline='' for deleting extra idle row
                w_vehicle = csv.writer(fnew)
                w_vehicle.writerow(headers)

                for row_v in r_vehicle:
                    # vehicle = Vehicle._make(row_v)
                    if row_v[0] == vehicleid:
                        w_vehicle.writerow([row_v[0], row_v[1], row_v[2], row_v[3],row_v[4], row_v[5], row_v[6], row_v[7], row_v[8]])


def run(filepath):
    '''aggregate all these functions and run this module
        
        filepath: 使用经过Geo Fence和计算并标记了POI的表的路径 
    '''
    nodeid_list = AllBusNodeid(filepath)
    seperate_vehicle(filepath, nodeid_list)
    print('Success!')

if __name__ == '__main__':
    filepath = 'fenced/fenced-2018-01-15.csv'
    run(filepath)




















