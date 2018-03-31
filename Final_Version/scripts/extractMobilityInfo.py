#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo


'''This program is to extract data for analysing mobility of vehicles

[description]: For each vehicle, service + start_service timing + round of service + duration
'''

import csv
import MyFunctions
import pprint
from decimal import Decimal


headers = ['node_id', 'vehicle_serial', 'date', 'time', 'speed', 'POI', 'service', 'service_start_stop', 'times of service', 'duration'] # 10
nodeid_times = {}  #{node_id: times}
nodeid_period = {}  #{node_id: [start_time, stop_time]}
nodeid_duration = {}  #{node_id: [duration1, duration2, ...]}

def calculateDuration(filepath):
    '''calculate duration
    
    Arguments:
        filepath {[String]} -- [eg: '../output/2017-09-04/final_2017-09-04.csv']
    '''
    with open(filepath, 'r') as f:
        r_f = csv.reader(f)
        headline = next(r_f)
        for row in r_f:
            # start
            if len(row) == 12 and row[11] != '':
                if row[11] == 'service_start':                            
                    date = row[2]
                    time = row[3].split('T')[1].split('.')[0]
                    if row[0] not in nodeid_times.keys():                                
                        nodeid_times[row[0]] = 0
                        nodeid_times[row[0]] += 1
                        nodeid_period[row[0]] = ['', '']
                        nodeid_period[row[0]][0] = time
                        nodeid_duration[row[0]] = []
                    else:
                        nodeid_times[row[0]] += 1
                        nodeid_period[row[0]][0] = time
                # stop 
                if row[11] == 'service_stop':
                    date = row[2]
                    time = row[3].split('T')[1].split('.')[0]                        
                    nodeid_period[row[0]][1] = time
                    if len(nodeid_period[row[0]]) == 2:
                        duration = MyFunctions.calculateDuration(nodeid_period[row[0]][0], nodeid_period[row[0]][1])
                        nodeid_duration[row[0]].append(duration)
                        nodeid_period[row[0]] = ['', '']
            else:
                continue
    # print(nodeid_duration)
    # print('SUCCESS 1')
    return(nodeid_duration)


def writeMobility(readFilePath, writeFilePath, nodeid_duration):
    '''Write Mobility Info
    
    Arguments:
        readFilePath {[String]} -- [Read the file from this path--eg: path of final_2017-09-04.csv]
        writeFilePath {[String]} -- [Write info into this file]
        nodeid_duration {[type]} -- [node_id -- duration]
    '''
    nodeid_times_w = {}
    with open(readFilePath, 'r') as f:
        r_f = csv.reader(f)
        headline = next(r_f)
        with open(writeFilePath, 'w', newline ='') as fnew:    #use 'w' for writing str and newline='' for deleting extra idle row
            w_fnew = csv.writer(fnew)
            w_fnew.writerow(headers)
            for row in r_f:
                # start
                if len(row) == 12 and row[11] != '':
                    if row[11] == 'service_start':
                        date = row[2]
                        time = row[3].split('T')[1].split('.')[0]
                        if row[0] not in nodeid_times_w.keys():                                
                            nodeid_times_w[row[0]] = 0
                            nodeid_times_w[row[0]] += 1                        
                        else:
                            nodeid_times_w[row[0]] += 1
                        try:
                            w_fnew.writerow([row[0], row[1], date, row[3], row[7], row[9], row[10], row[11], nodeid_times_w[row[0]], nodeid_duration[row[0]][nodeid_times_w[row[0]]-1]])
                        except IndexError as e:
                            print('Lose data indicating the end of service. No way to get the value of duration.')


    print('Generate mobility file successfully')


def normalizeDuration(filepath):
    '''It seems that there is no need to use this function'''
    with open(filepath, 'r+') as f:
        r_f = csv.reader(f)
        header = next(r_f)
        w_f = csv.writer(f)
        for row in r_f:
            # print(row)
            if len(row) == 12 and row[11] != '':
                if len(row[10].split(':')) == 3:
                    row[10] = row[10][0:5]
                    w_f.writerow([row[0], row[1], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]])
    print('SUCCESS 3')


def run_RTT(folderpath):
    '''Run
    
    Arguments:
        filepath {[String]} -- [eg: '../output/2017-09-04/final_2017-09-04.csv']
    '''
    fileName = MyFunctions.visitAllFile(folderpath)
    if '.DS_Store' in fileName[0]:
        fileName[0].pop(fileName[0].index('.DS_Store'))
    print('Modified file list is: ', fileName[0])
    print('------ There are %d files ------' %len(fileName[0]))
    count = 1
    for item in fileName[0]:
        filepath = folderpath + '/' + item
        print('This is %d file out of %d' %(count, len(fileName[0])))
        nodeid_duration = calculateDuration(filepath)
        count += 1
        # filepath_nor = 'Mobility/mobility_2017-09-05.csv' 
        # normalizeDuration(filepath_nor)
        
        filename = 'mobility_' + filepath.split('/')[-1].split('_')[1]
        newpath = '../mobility/' + filename
        print(newpath)
        MyFunctions.checkPath(newpath)
        writeMobility(filepath, newpath, nodeid_duration)

if __name__ == '__main__':

    folderpath = '../output'

    run(folderpath)




