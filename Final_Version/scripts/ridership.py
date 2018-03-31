#!/usr/bin/python
# -*-coding: UTF-8-*-

import psycopg2
#为了使用dictcursor
import psycopg2.extras
import csv
import datetime 
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


def ridership(database,user,password,host,port):
	

	bus_ID = ['2023','2024','2025','2026','2027','2028','2029','2030','2031','2032','2033','2034','2035','2036','2037',\
          '2038','2039','2040','2041','2042','2043','2044','2045','2046','2047','2048','2049','2050','2051','2052',\
          '2053','2054','2055','2056','2057','2058','2059','2060','2061','2062','2063','2064','2065','2066','2067',\
          '2068','2069','2070','2071','2072','2073','2074','2075','2076','2077','2078','2079','2080','2102','2129']

	# find all the processed mobility data
	filelist_bus = search('C:\\Users\\HXY\\Desktop\\demo1\\output','final')

	# 提取processed mobility csv file的日期
	date = []
	for i in range(len(filelist_bus)):
		date.append(filelist_bus[i].split('\\')[-1].split('_')[-1].split('.')[0])

	# find the corresponding session data file
	for day in date:
		file_session = search('C:\\Users\\HXY\\Desktop\\demo1\\Download',day)
		# 如果找不到文件就跳过
		if len(file_session) == 0:
			print('No session data for '+day);
			continue
		# 找到对应的mobility csv
		file_bus = search('C:\\Users\\HXY\\Desktop\\demo1\\output',day)

		# 数据库连接参数
		conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
		# cur = conn.cursor()
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		# cur.execute("DROP TABLE ridership;")
		# cur.execute("DROP TABLE mobility;")

		#建表
		tablename = 'ridership_'+day.replace('-','_')
		SQL = "CREATE TABLE "+tablename+" (node_id TEXT NOT NULL,vehicle_serial TEXT NOT NULL, date  date  NOT NULL,gps_time  TEXT    NOT NULL,latitude TEXT NOT NULL,longitude TEXT NOT NULL,altitude TEXT NOT NULL,speed TEXT NOT NULL,heading TEXT NOT NULL, Num_Dev NUMERIC NOT NULL, POI     TEXT    NOT NULL,service     TEXT,service_start_stop        TEXT,PRIMARY KEY(node_id,date,gps_time));"
		cur.execute(SQL)

		bus_raw = []
		session_raw = []
		# 读取相应的mobility文件数据
		with open(file_bus[0],'r') as mobility:
			reader = csv.DictReader(mobility)
			for row in reader:
				bus_raw.append(row)

		# 读取相应的session文件数据
		with open(file_session[0],'r') as session:
			reader = csv.DictReader(session)
			for row in reader:
				session_raw.append(row)

		for n in range(len(bus_ID)):
			print(n)
			bus=[]
			bus_1=[]
			device_1=[]
		     
		    
			for i in range(len(bus_raw)):
				if bus_raw[i]['node_id']==bus_ID[n]:
					bus.append(bus_raw[i])    
		    #sort by time
			bus=sorted(bus, key=lambda x:x['gps_time'])
			for i in range(len(bus)):
		        # discard bus data with the same time
				if i==0 or bus[i]['gps_time'] != bus[i-1]['gps_time']:  
					bus_1.append(dict(bus[i]))
		            
			if not(bus_1):
				continue
			else:
				node = bus_1[0]['node_id']

			for i in range(len(session_raw)):
				if session_raw[i]['gw_id']==node:
		            # filter out abnormal device data
					if session_raw[i]['duration']!='null' and int(session_raw[i]['duration'])>=0: 
						device_1.append(dict(session_raw[i]))
		    
		    # transfer GWT to Singapore time
			for i in range (len(bus_1)):
				bus_1[i]['gps_time']=datetime.datetime.strptime(bus_1[i]['gps_time'],"%Y-%m-%dT%H:%M:%S.000Z")
				bus_1[i]['mac_hash']=[]
		    # transfer GWT to Singapore time
			for i in range (len(device_1)):
				device_1[i]['ts_begin']=datetime.datetime.strptime(device_1[i]['ts_begin'],"%Y-%m-%dT%H:%M:%S.000Z")+datetime.timedelta(hours=8)  
			
			for j in range(len(device_1)):		            
				for i in range(len(bus_1)):
					if bus_1[i]['gps_time'] >= device_1[j]['ts_begin']:
						if bus_1[i]['gps_time'] <= device_1[j]['ts_begin'] + datetime.timedelta(seconds=int(device_1[j]['duration'])):
							bus_1[i]['mac_hash'].append(device_1[j]['mac_hash'])
						else:
							break
			for i in range (len(bus_1)):
				bus_1[i]['mac_hash']=list(set(bus_1[i]['mac_hash']))
				bus_1[i]['Num_Dev']=len(bus_1[i]['mac_hash'])
				d={'node_id':bus_1[i]['node_id'],'vehicle_serial':bus_1[i]['vehicle_serial'],'date':bus_1[i]['gps_time'].strftime("%Y-%m-%d"),'gps_time':bus_1[i]['gps_time'].strftime("%Y-%m-%dT%H:%M:%S"),'latitude':bus_1[i]['latitude'],'longitude':bus_1[i]['longitude'],'altitude':bus_1[i]['altitude'],'speed':bus_1[i]['speed'],'heading':bus_1[i]['heading'],'Num_Dev':bus_1[i]['Num_Dev'],'POI':bus_1[i]['POI'],'service':bus_1[i]['service'],'service_start_stop':bus_1[i]['service_start_stop']}
		        # dict=(bus_1[i]['node_id'],bus_1[i]['gps_time'].strftime("%Y-%m-%d %H:%M:%S"),bus_1[i]['Num_Dev'])
				cur.execute("INSERT INTO "+tablename+" VALUES(%(node_id)s,%(vehicle_serial)s,%(date)s,%(gps_time)s,%(latitude)s,%(longitude)s,%(altitude)s,%(speed)s,%(heading)s,%(Num_Dev)s,%(POI)s,%(service)s,%(service_start_stop)s)", d) 
			print(day+' : '+str(bus_ID[n])+' completed.')
		print(day+' : All buses completed.')
		
		conn.commit()
		cur.close()
		conn.close()
	print('The whole week completed.')
	return


if __name__ == '__main__':
	# ridership analysis
	database="ridership"
	user="postgres"
	password="HXYHXKWY950118!"
	host="localhost"
	port="5432"
	ridership(database,user,password,host,port)