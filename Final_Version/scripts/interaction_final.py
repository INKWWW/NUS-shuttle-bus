#!/usr/bin/python
# -*-coding: UTF-8-*-
# @Author :Wang Hanmo

import tkinter as tk
import execution

# function

def confirmInput():
    start = var_start_date.get()
    stop = var_stop_date.get()
    result = start + '~' + stop
    display_result = 'You have chosen the Range: ' + result
    dis.insert('insert', display_result)
    # 此处导入程序对数据进行处理
    execution.execution(result)
    

def clearInput():
    var_start_date.set('')
    var_stop_date.set('')
    dis.delete(0.0, 'end')

win = tk.Tk()
win.title('Choose the date')
win.geometry('500x400')

# NUS AMI LAB
l1 = tk.Label(win, text='NUS AMI LAB', font=('Arial', 30))
l1.place(x=160,y=60)
l2 = tk.Label(win, text='NUS Shuttle Bus Analytics', font=('Arial', 20))
l2.place(x=140,y=100)

# start and stop
start_label = tk.Label(win, text='Start_date: ').place(x=80, y=150)
stop_label = tk.Label(win, text='Stop_date: ').place(x=80, y=190)

var_start_date = tk.StringVar()
var_start_date.set('eg.2017-09-04')
var_stop_date = tk.StringVar()
var_stop_date.set('eg.2017-09-06')

# input
entry_start_date = tk.Entry(win, textvariable=var_start_date, show=None, width=20)
entry_start_date.place(x=200, y=150)

entry_stop_date = tk.Entry(win, textvariable=var_stop_date, show=None, width=20)
entry_stop_date.place(x=200, y=190)

# confirm button
btn_con = tk.Button(win, text='Confirm', command=confirmInput)
btn_con.place(x=180, y=230)

# clear button
btn_cl = tk.Button(win, text='Clear', command=clearInput)
btn_cl.place(x=300, y=230) 

# display
dis = tk.Text(win, height=2)
dis.place(x=60, y=280)

win.mainloop()


