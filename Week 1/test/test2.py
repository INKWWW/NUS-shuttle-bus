#!/usr/bin/python
# -*-coding: UTF-8-*-

#按照column读取
    # for index, rows in enumerate (f_csv):
    # 	if index == 1:
    # 		row = rows
    # print (row)

from collections import namedtuple
import csv

vehicleid = input('please input the vehicleid: ')  
headers = ['gps_time', 'latitude', 'longitude', 'altitude', 'speed', 'heading',\
			'session_id', 'mac_hash', '# of device']
counter = 0


#read the data from vehicle
with open('2017-08-28-vehicle.csv', 'r') as f_vehicle_r:
	f_vehicle = csv.reader(f_vehicle_r)
	headings_v = next(f_vehicle)
	# print (headings)
	Row_vehicle = namedtuple('Row_vehicle', headings_v)  #namedtuple让row读取的时候可以带上属性，更明确	
	print ('vehicle_success')

	with open('2017-08-28-device.csv', 'r') as f_device_r:
		f_device = csv.reader(f_device_r)
		headings_d = next(f_device)
		Row_device = namedtuple('Row_device', headings_d)		
		print ('device_success')

		with open('newcsvfile2.csv', 'w') as f_w:
			f_writer = csv.writer(f_w)
			f_writer.writerow(headers)
			for r_v in f_vehicle:
				row_v = Row_vehicle(*r_v)
				# print(row_v.node_id)
				for r_d in f_device:
					row_d = Row_device(*r_d)
					# print(row_d.gw_id)			
			# print('check 1')
				if row_d.gw_id == vehicleid:
					f_writer.writerow([r_d[1]])
		

			# for gw_id in row_d.gw_id:
			# 	print(gw_id)

			# while row_d.gw_id == vehicleid and row_v.node_id == vehicleid:
			# 	print ('check 2')
			# 	if row_d.ts_begin == row_v.gps_time:
			# 		print ('get it')
			# 		# counter = counter + 1
			# 		f_writer.writerow('','','','','','',r_d[0])


	# with open('newcsvfile2.csv', 'w') as f_w:
	# 	fv_writer = csv.writer(f_w)
	# 		if row_v.node_id == vehicleid:
	# 			print(r_v[0],r_v[1])
	# 			fv_writer.writerow([r_v[2],r_v[3],r_v[4],r_v[5],r_v[6],r_v[7]])

	# f_vehicle_w.close()
#f_vehicle_r.close()

#read the data from the devices
	
		















