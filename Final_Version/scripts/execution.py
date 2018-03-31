#!/usr/bin/python
# -*-coding: UTF-8-*-
import web
import aggregate
import ridership
import extractMobilityInfo
import mobilityInterval
import upload
import datetime 
import math



def execution(result):
	# 获取起止日期
	result = result.split('~')
	date_begin = result[0]
	date_end = result[-1]
	date_end = datetime.datetime.strptime(date_end,"%Y-%m-%d")

	# 获取所有选中日期
	day_range = []
	date = datetime.datetime.strptime(date_begin,"%Y-%m-%d")
	while date <= date_end:
		day_range.append(date.strftime("%Y-%m-%d"))
		date = date + datetime.timedelta(days=1)
	# download the raw data
	date = datetime.datetime.strptime(date_begin,"%Y-%m-%d")
	web.update(date.strftime("%Y-%m-%d"))
	
	while (date + datetime.timedelta(days=7)) <= date_end:
		date = date + datetime.timedelta(days=7)
		web.update(date.strftime("%Y-%m-%d"))	

	# 删除选中日期以外的文件
	path = '../Download/'
	word = 'BusLocation'
	Bus_dir = web.search_dir(path, word)	
	for i in Bus_dir:
		web.del_file(i,day_range)
	word = 'Session'
	Session_dir = web.search_dir(path, word)	
	for i in Session_dir:
		web.del_file(i,day_range)
	
	# service recognition
	word = 'BusLocation'
	Bus_dir = web.search_dir(path, word)
	for filedir_bus in Bus_dir:
		#### Modify folderpath ####
		aggregate.aggregate(filedir_bus)

	# ridership analysis
	database="ridership"
	user="postgres"
	password="NUSBUS"
	host="localhost"
	port="5432"
	ridership.ridership(database,user,password,host,port)

	# round trip time
	folderpath = '../output'
	database="RTT"
	extractMobilityInfo.run_RTT(folderpath)
	upload.RTT_upload(database,user,password,host,port)
	

	# interarrival
	database="inter_arrival"
	mobilityInterval.run_interarrival(folderpath)
	upload.inter_arrival_upload(database,user,password,host,port)
	
	web.clean()
	print('COMPLETED!')
	return

# if __name__ == '__main__':
# 	execution(result)
	