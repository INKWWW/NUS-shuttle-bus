#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

'''Aggregate all part and run them in this .py file

'''

import MyFunctions
import fence_NUS
import DetermineService
import determinePoi
import advancedDetermineService


if __name__ == '__main__':

    # first step 
    filepath_fence = '../Veniam_BusLocation/2017_week36/2017-09-05.csv'
    fence_NUS.run(filepath_fence)
    print('first step successfully')

    # # second step
    filepath_detepoi = '../Veniam_BusLocation/2017_week36/2017-09-05.csv'
    determinePoi.run(filepath_detepoi)
    print('second step successfully')

    # third step
    folderpath = 'fenced_vehicle/2017-09-05'
    read_filepath = 'fenced/fenced-2017-09-05.csv'
    write_filepath = 'Final_Result/final_2017-09-05.csv'
    advancedDetermineService.run(folderpath, read_filepath, write_filepath)
    print('third step successfully')







