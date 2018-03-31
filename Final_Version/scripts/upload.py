#!/usr/bin/python
# -*-coding: UTF-8-*-

import psycopg2
#为了使用dictcursor
import psycopg2.extras
import csv
import os
import sys

def search(path, word):
	r = []
	for filename in os.listdir(path):
		fp = os.path.join(path, filename)
		if os.path.isfile(fp) and word in filename:
			#print('yes:'+fp)
			r.append(fp)
		elif os.path.isdir(fp):
			#print('no:'+fp)
			r = search(fp, word)
	return r

def RTT_upload(database,user,password,host,port):
	# find all the processed mobility data
	filelist_bus = search('C:\\Users\\HXY\\Desktop\\demo1\\output','final')

	# 提取processed mobility csv file的日期
	date = []
	for i in range(len(filelist_bus)):
		date.append(filelist_bus[i].split('\\')[-1].split('_')[-1].split('.')[0])

	# find the corresponding RTT data file
	for day in date:
		file_RRT = search('C:\\Users\\HXY\\Desktop\\demo1\\mobility',day)
		# 如果找不到文件就跳过
		if len(file_RRT) == 0:
			print('No RTT data for '+day);
			continue
		# 数据库连接参数
		conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
		# cur = conn.cursor()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		# cur.execute("DROP TABLE ridership;")
		# cur.execute("DROP TABLE mobility;")

		#建表
		tablename = 'RTT_'+day.replace('-','_')
		SQL = "CREATE TABLE "+tablename+" (node_id TEXT NOT NULL,vehicle_serial TEXT NOT NULL, date  date  NOT NULL,time  TEXT    NOT NULL,speed TEXT NOT NULL,POI     TEXT    NOT NULL,service     TEXT,service_start_stop        TEXT,times_of_service TEXT NOT NULL, duration TEXT NOT NULL,PRIMARY KEY(node_id,date,time));"
		cur.execute(SQL)
		#upload the data
		cur.execute("COPY "+tablename+" FROM \'"+file_RRT[0]+"\' WITH CSV HEADER;")

		conn.commit()
		cur.close()
		conn.close()
	return

def inter_arrival_upload(database,user,password,host,port):
	# find all the processed mobility data
	filelist_bus = search('C:\\Users\\HXY\\Desktop\\demo1\\output','final')

	# 提取processed mobility csv file的日期
	date = []
	for i in range(len(filelist_bus)):
		date.append(filelist_bus[i].split('\\')[-1].split('_')[-1].split('.')[0])

	# find the corresponding RTT data file
	for day in date:
		file_inter_arrival = search('C:\\Users\\HXY\\Desktop\\demo1\\interval',day)
		# 如果找不到文件就跳过
		if len(file_inter_arrival) == 0:
			print('No RTT data for '+day);
			continue
		# 数据库连接参数
		conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
		# cur = conn.cursor()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		# cur.execute("DROP TABLE ridership;")
		# cur.execute("DROP TABLE mobility;")

		#建表
		tablename = 'inter_arrival_'+day.replace('-','_')
		SQL = "CREATE TABLE "+tablename+" (node_id TEXT NOT NULL,vehicle_serial TEXT NOT NULL, date  date  NOT NULL,time  TEXT    NOT NULL,POI     TEXT    NOT NULL,service     TEXT, interval TEXT NOT NULL,PRIMARY KEY(node_id,date,time));"
		cur.execute(SQL)
		#upload the data
		cur.execute("COPY "+tablename+" FROM \'"+file_inter_arrival[0]+"\' WITH CSV HEADER;")

		conn.commit()
		cur.close()
		conn.close()
	return