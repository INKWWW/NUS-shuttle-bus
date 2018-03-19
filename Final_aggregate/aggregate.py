#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

'''Aggregate all part and run them in this .py file

'''

import MyFunctions
import determinePoi
import seperate_vehicle
import determineServiceF1

def handleEachFile(filepath):
    '''Handle each file
    
    Arguments:
        filepath {[String]} -- [raw file path] # ‘../Download/BusLocation_09_05_2017/2017-09-04.csv’
    '''
    # First step
    determinePoi.run(filepath) # ‘../Download/BusLocation_09_05_2017/2017-09-04.csv’
    print('First step successfully')

    # Second step
    filepath2 = 'fenced/fenced-' + filepath.split('/')[-1] # 'fenced/fenced-2017-09-04.csv'
    seperate_vehicle.run(filepath2)
    print('Second step successfully')

    # Third step
    folderpath = 'fenced_vehicle/' + filepath.split('/')[-1].split('.')[0] # 'fenced_vehicle/2017-09-04'
    read_filepath = filepath2
    write_filepath = '../output/' + 'final_' + filepath.split('/')[-1]
    # write_filepath = '../output/' + filepath.split('/')[-1].split('.')[0] + '/' + 'final_' + filepath.split('/')[-1]
    # MyFunctions.checkPath(write_filepath)

    determineServiceF1.run(folderpath, read_filepath, write_filepath)
    print('Third step successfully')


def aggregate(folderpath):
    '''Aggregate scripts here
    
    Arguments:
        folderpath {[String]} -- [the folder containing all raw files]
    '''
    fileNameList = MyFunctions.visitAllFile(folderpath) # fileNameList = [[]]
    numOfFiles = len(fileNameList[0])
    print('There are %d files in this folder' %numOfFiles)

    count = 1
    for filepath in fileNameList[0]:
        print('This is %d file out of %d files' %(count, len(fileNameList[0])))
        print('Please wait for file %d\'s process...' %count)
        filepath_new = folderpath + '/' + filepath # ‘../Download/BusLocation_09_05_2017/2017-09-04.csv’
        handleEachFile(filepath_new)
        count += 1
    # Delete the folder generated in this process
    # 'Fenced' & 'fenced_vehicle'
    MyFunctions.deleteFolder('fenced')
    MyFunctions.deleteFolder('fenced_vehicle')
    print('Complete successfully')


if __name__ == '__main__':

    #### Modify folderpath ####
    folderpath = '../Download/BusLocation_09_05_2017'
    aggregate(folderpath)






