from skmultiflow.drift_detection import ADWIN

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import psycopg2
import pandas as pd
import numpy as np
from statistics import mean
import datetime as dt
import requests

fig = plt.figure()
y_real = []
y_avg = []
window_size=10
title=['Real Data Input','Average Windows Size:'+str(window_size)]

url = 'https://notify-api.line.me/api/notify'
token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

connection = None
cursor = None
drift_detector = ADWIN()

def line_notify(msg):
    r = requests.post(url, headers=headers, data = {'message':msg})
    print (r.text)

def animate(i,y_real, y_avg):
    #print('..........11')
    print('detection......:',dt.datetime.now().strftime('%H:%M:%S.%f'))
    data=[]
    try:
        connection = psycopg2.connect(
            user='admin',
            password='quest',
            host='192.168.1.19',
            port='8812',
            database='qdb')
        cursor = connection.cursor() 
        postgreSQL_select_Query = 'SELECT bn_last FROM \'topic_Binance_Bitkub\' ORDER BY timestamp DESC LIMIT 500'  # preiod 30-40 minutes
        cursor.execute(postgreSQL_select_Query)
        data = cursor.fetchall()
        data.reverse()
        '''........................'''
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        #print("PostgreSQL connection is closed")
    
    data1=[]
    for i,res in enumerate(data):
        data1.append(res[0])
    #print('..........',data2)    
    size = window_size
    data2 = []
    i = 0
    while i < len(data):
        val = np.mean(data[i:i+3])
        data2.append(val)
        i+=size

    stream = np.array(data2)
    for i, val in enumerate(stream):
        drift_detector.add_element(val)
        #print(i,val,drift_detector.detected_change())        # Data is processed one sample at a time
        if drift_detector.detected_change():
            print('Change detected at index {} of {}'.format(i,len(data2)))
            msg='BNB Detection prices {:.2f} ,latest {:.2f} ,mean {:.2f} ,max {:.2f} and min {:.2f}.'.format(data2[i],
            data2[-1],mean(data1),max(data1),min(data1))
            
            print(msg)
            if data2[i]<mean(data1) and data2[-1]<mean(data1):
                line_notify("Going down...")
                line_notify(msg)
            elif data2[i]>mean(data1) and data2[-1]>mean(data1):
                line_notify("Going up...")
                line_notify(msg)
                        
            drift_detector.reset()

    #print('!!!!!!!',data1)     
    for i in range(1, 3):
        ax = plt.subplot(1, 2, i)
        ax.clear()
        ax.plot(eval('data%d'% (i)))
        plt.xticks(rotation=45, ha='right')
        ax.set_title(title[i-1])
        ax.set_ylabel('Prices')


ani = animation.FuncAnimation(fig, animate, fargs=(y_real, y_avg),interval=60000)
plt.show()
