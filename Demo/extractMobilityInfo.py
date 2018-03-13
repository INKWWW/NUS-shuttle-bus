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


headers = ['node_id', 'vehicle_serial', 'date', 'time', 'speed', 'POI', 'service', 'service_start_stop', 'times of service', 'duration']
nodeid_times = {}  #{node_id: times}
nodeid_period = {}  #{node_id: [start_time, stop_time]}
nodeid_duration = {}  #{node_id: [duration1, duration2, ...]}

def calculateDuration(filepath):
    with open(filepath, 'r') as f:
        r_f = csv.reader(f)
        headline = next(r_f)
        for row in r_f:
            # start
            if len(row) == 11:
                if row[10] == 'service_start':                            
                    date = row[2].split('T')[0]
                    time = row[2].split('T')[1].split('.')[0]
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
                if row[10] == 'service_stop':
                    date = row[2].split('T')[0]
                    time = row[2].split('T')[1].split('.')[0]                        
                    nodeid_period[row[0]][1] = time
                    if len(nodeid_period[row[0]]) == 2:
                        duration = MyFunctions.calculateDuration(nodeid_period[row[0]][0], nodeid_period[row[0]][1])
                        # pprint.pprint(nodeid_period)
                        # if int(nodeid_period[row[0]][1].split(':')[2]) < int(nodeid_period[row[0]][0].split(':')[2]):
                        #     period_sec = 60 - (int(nodeid_period[row[0]][0].split(':')[2]) - int(nodeid_period[row[0]][1].split(':')[2]))
                        #     period_min = int(nodeid_period[row[0]][1].split(':')[1]) - int(nodeid_period[row[0]][0].split(':')[1]) - 1
                        #     if period_min < 0:
                        #         period_min = 60 + period_min
                        # else:
                        #     period_sec = int(nodeid_period[row[0]][1].split(':')[2]) - int(nodeid_period[row[0]][0].split(':')[2])
                        #     period_min = int(nodeid_period[row[0]][1].split(':')[1]) - int(nodeid_period[row[0]][0].split(':')[1])
                        #     if period_min < 0:
                        #         period_min = 60 + period_min
                        # # duration = ':'.join([str(period_min), str(period_sec)])
                        # duration = str(round(period_min + (period_sec / 60), 2))
                        nodeid_duration[row[0]].append(duration)
                        nodeid_period[row[0]] = ['', '']
            else:
                continue
    print(nodeid_duration)
    print('SUCCESS 1')
    return(nodeid_duration)


def writeMobility(readFilePath, writeFilePath, nodeid_duration):
    nodeid_times_w = {}
    with open(readFilePath, 'r') as f:
        r_f = csv.reader(f)
        headline = next(r_f)
        with open(writeFilePath, 'w', newline ='') as fnew:    #use 'w' for writing str and newline='' for deleting extra idle row
            w_fnew = csv.writer(fnew)
            w_fnew.writerow(headers)
            for row in r_f:
                # start
                if len(row) == 11:
                    if row[10] == 'service_start':
                        date = row[2].split('T')[0]
                        time = row[2].split('T')[1].split('.')[0]
                        if row[0] not in nodeid_times_w.keys():                                
                            nodeid_times_w[row[0]] = 0
                            nodeid_times_w[row[0]] += 1                        
                        else:
                            nodeid_times_w[row[0]] += 1
                        # print('nodeid_time_w', nodeid_times_w)

                        # print(nodeid_duration[row[0]][nodeid_times_w[row[0]]-1])
                        w_fnew.writerow([ row[0], row[1], date, time, row[6], row[8], row[9], row[10], nodeid_times_w[row[0]], nodeid_duration[row[0]][nodeid_times_w[row[0]]-1] ])
                        # except IndexError as e:
                        #     print(e)
                        #     w_fnew.writerow([row[0], row[1], date, time, row[6], row[8], row[9], row[10], nodeid_times[row[0]], nodeid_duration[row[0]][nodeid_times[row[0]]]])
    print('SUCCESS 2')


def normalizeDuration(filepath):
    with open(filepath, 'r+') as f:
        r_f = csv.reader(f)
        header = next(r_f)
        w_f = csv.writer(f)
        for row in r_f:
            # print(row)
            if len(row) == 10:
                if len(row[9].split(':')) == 3:
                    row[9] = row[9][0:5]
                    w_f.writerow([row[0], row[1],row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
    print('SUCCESS 2')


if __name__ == '__main__':
    filepath = 'Final_Result/final_2017-09-05.csv'
    nodeid_duration = calculateDuration(filepath)
    # filepath_nor = 'Mobility/mobility_2017-09-05.csv' 
    # normalizeDuration(filepath_nor)
    
    filename = 'mobility_' + filepath.split('/')[1].split('_')[1]
    newpath = '/'.join([ 'Mobility', filename ])
    print(newpath)
    MyFunctions.checkPath(newpath)
    writeMobility(filepath, newpath, nodeid_duration)








