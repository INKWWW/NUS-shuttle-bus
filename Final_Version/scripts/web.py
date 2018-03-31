#!/usr/bin/python
# -*-coding: UTF-8-*-

import urllib
from selenium import webdriver
import time
from time import sleep
import os
import sys
import zipfile
import datetime 
import re



def download(Username,Password,category,Startdate,path):
	# 禁止弹出窗口，设置默认下载路径
	options = webdriver.ChromeOptions()
	prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': path}
	options.add_experimental_option('prefs', prefs)


	chromedriver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"  
	browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options) 

	#登录页面
	url = r'https://datacommons.nus.edu.sg/Default'

	# 访问登录页面
	browser.get(url)

	# 等待一定时间，让js脚本加载完毕
	browser.implicitly_wait(3)

	#输入用户名
	username = browser.find_element_by_xpath(r'//*[@id="MainContent_UserName"]')
	username.send_keys(Username)

	#输入密码
	password = browser.find_element_by_name(r'ctl00$MainContent$Password')
	password.send_keys(Password)

	#点击“登录”按钮
	login_button = browser.find_element_by_name(r'ctl00$MainContent$btnLogin')
	login_button.click()

	#拉开面板
	data_panel=browser.find_element_by_xpath(r'//*[@id="accordion"]/div[3]/a')
	data_panel.click()

	history_active=browser.find_element_by_xpath(r'//*[@id="collapse3"]/div/ul/li[2]')
	history_active.click()

	if category == 'BusLocation':
		category_active=browser.find_element_by_xpath(r'//*[@id="BusArchive"]/div/div[3]/label/input')
		category_active.send_keys('Shuttle Bus Mobility')
	if category == 'Session':
		category_active=browser.find_element_by_xpath(r'//*[@id="BusArchive"]/div/div[4]/label/input')
		category_active.send_keys('WiFi Device Sessions')

	start_week = browser.find_element_by_name(r'txtBusStartDate')
	start_week.send_keys(Startdate)

	end_week = browser.find_element_by_name(r'txtBusEndDate')
	end_week.click()

	download = browser.find_element_by_name(r'ctl00$MainContent$btnBus')
	download.click()
	# urllib.request.urlretrieve(r'https://datacommons.nus.edu.sg/Handler.ashx?path=\\fs9.nus.edu.sg\DATACOMM\weekly_archive\veniam\bus_location', "data.zip")
	# #网页截图
	# browser.save_screenshot('picture1.png')
	#打印网页源代码
	#print(browser.page_source.encode('utf-8').decode())
	# 等待一定时间
	sleep(30)
	# #关闭浏览器
	browser.quit()
	return

# 查询目录及其子目录中的含有某关键字的文件
def search(path, word):
	r = []
	for filename in os.listdir(path):
		fp = os.path.join(path, filename)
		if os.path.isfile(fp) and word in filename:
			print('yes:'+fp)
			r.append(fp)
		elif os.path.isdir(fp):
			print('no:'+fp)
			r = search(fp, word)
	return r

# 查询含有某关键字的目录
def search_dir(path, word):
	r = []
	for filename in os.listdir(path):
		fp = os.path.join(path, filename)
		if os.path.isdir(fp) and word in filename:
			print('yes:'+fp)
			r.append(fp)
	return r


def decompress(path,date,fp,category):
	filedir = path + category + '_' + date  + '/'  #解压后放入的目录
	r = zipfile.is_zipfile(fp)
	if r:
	    fz = zipfile.ZipFile(fp,'r')
	    for file in fz.namelist():
	    	fz.extract(file,filedir)
	else:
	    print('This file is not zip file')
	return

def clear_file(path):
	for i in os.listdir(path):
		path_file = os.path.join(path,i)  #取文件绝对路径
		if os.path.isfile(path_file):
			os.remove(path_file)
		else:
			clear_file(path_file)
	# 删除所有空目录
	os.rmdir(path) 
	return

def clean():
	# 删除download文件
	path = os.getcwd().split('scripts')[0] + 'Download\\'
	word = 'BusLocation'
	Bus_dir = search_dir(path, word)	
	for i in Bus_dir:
		clear_file(i)
	word = 'Session'
	Session_dir = search_dir(path, word)	
	for i in Session_dir:
		clear_file(i)

	# 删除output文件
	path = '../output/'
	word = '-'
	file = search(path, word)	
	for i in file:
		path_file = os.path.join(path,i)  #取文件绝对路径
		if os.path.isfile(path_file):
			os.remove(path_file)

	# 删除mobility文件
	path = '../mobility/'
	word = '-'
	file = search(path, word)	
	for i in file:
		path_file = os.path.join(path,i)  #取文件绝对路径
		if os.path.isfile(path_file):
			os.remove(path_file)

	# 删除interval文件
	path = '../interval/'
	word = '-'
	file = search(path, word)	
	for i in file:
		path_file = os.path.join(path,i)  #取文件绝对路径
		if os.path.isfile(path_file):
			os.remove(path_file)

	return


# def load(path,date):
# 	database="raw_data"
# 	user="postgres"
# 	password="HXYHXKWY950118!"
# 	host="localhost"
# 	port="5432"

# 	# 数据库连接参数
# 	conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
# 	# cur = conn.cursor()
# 	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# 	filedir_bus = path + 'BusLocation' + '_' + date + '\\'  #解压后放入的目录
# 	for filename in os.listdir(filedir_bus):
# 		tablename = 'BusLocation_' + filename.replace('-','_').replace('.csv','')
# 		# cur.execute("DROP TABLE "+tablename+";")
# 		#建表
# 		build_table = "CREATE TABLE " + tablename + "(node_id			TEXT	NOT NULL,vehicle_serial		TEXT	NOT NULL,gps_time		TEXT	NOT NULL,latitude		TEXT	NOT NULL,longitude		TEXT	NOT NULL,altitude		TEXT	NOT NULL,speed			TEXT	NOT NULL,heading			TEXT	NOT NULL);"
# 		cur.execute(build_table)
# 		cur.execute("COPY " + tablename + " FROM \'" + filedir_bus + filename + "\' WITH CSV HEADER;")
# 		print(tablename)

# 	filedir_session = path + 'Session' + '_' + date + '\\'  #解压后放入的目录
# 	for filename in os.listdir(filedir_session):
# 		tablename = 'Session_' + filename.replace('-','_').replace('.csv','')
# 		# cur.execute("DROP TABLE "+tablename+";")
# 		#建表
# 		build_table = "CREATE TABLE " + tablename + "(session_id		TEXT	NOT NULL,mac_hash		TEXT	NOT NULL,gw_id			TEXT	NOT NULL,ts_begin		TEXT	NOT NULL,ts_end			TEXT,incoming		TEXT	NOT NULL,outgoing		TEXT	NOT NULL,latitude_begin		TEXT	NOT NULL,longitude_begin		TEXT	NOT NULL,latitude_end		TEXT	NOT NULL,longitude_end		TEXT	NOT NULL,duration		TEXT	NOT NULL);"
# 		cur.execute(build_table)
# 		cur.execute("COPY " + tablename + " FROM \'" + filedir_session + filename + "\' WITH CSV HEADER;")
# 		print(tablename)
# 	conn.commit()
# 	cur.close()
# 	conn.close()

# 	return

def del_file(path,day_range):
	for i in os.listdir(path):
		path_file = os.path.join(path,i)  #取文件绝对路径
		# 删除选中日期范围以外的文件
		if os.path.isfile(path_file):
			filename = i.split('.')[0]
			if filename in day_range:
				pass
			else:
				print('remove'+filename)
				os.remove(path_file)
		else:
			print('Not a file!')
	return


def update(date):
	# account information
	Username = r'1072780189@qq.com'
	Password = r'NUSbus111'
	# Startdate = r'09/05/2017'
	word_1 = 'Zip_Veniam_BusLocation'
	word_2 = 'Zip_Veniam_Session'
	word_3 = 'week'

	path = os.getcwd().split('scripts')[0] + 'Download/'
	category = 'BusLocation'#'Session'
	# date = '09_05_2017'
	year = date.split('-')[0]
	month = date.split('-')[1]
	day = date.split('-')[2]
	Startdate = month + '/' + day + '/' + year


	download(Username,Password,category,Startdate,path)
	fp_zip = search(path, word_1)
	decompress(path+'_temp_',date,fp_zip[0],category)
	fp = search(path, word_3)
	decompress(path,date,fp[0],category)
	clear_file(path +'_temp_'+ category + '_' + date  + '/')
	os.remove(fp_zip[0])

	category = 'Session'#'BusLocation'
	download(Username,Password,category,Startdate,path)
	fp_zip = search(path, word_2)
	decompress(path+'_temp_',date,fp_zip[0],category)
	fp = search(path, word_3)
	decompress(path,date,fp[0],category)
	clear_file(path +'_temp_'+ category + '_' + date  + '/')
	os.remove(fp_zip[0])

	# load(path,date)
	return

# if __name__ == '__main__':
# 	update('2017-09-11')
