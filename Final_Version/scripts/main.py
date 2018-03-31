#!/usr/bin/python
# -*-coding: UTF-8-*-

import web
import aggregate
import ridership
import extractMobilityInfo
import mobilityInterval
import upload

def execution(result):
	# download the raw data
	update(date_begin,date_end)

	#### Modify folderpath ####
	folderpath = '../Download/BusLocation_09_05_2017'
	aggregate(folderpath)

	# ridership analysis
	database="ridership"
	user="postgres"
	password="HXYHXKWY950118!"
	host="localhost"
	port="5432"
	ridership(database,user,password,host,port)

	# round trip time
	folderpath = '../output'
	database="RTT"
	RTT_upload(database,user,password,host,port)
	run_RTT(folderpath)

	# interarrival
	database="inter_arrival"
	inter_arrival_upload(database,user,password,host,port)
	run_interarrival(folderpath)
	return

	
	