#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:27:28 2020

@author: sruthi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:05:03 2020

@author: sruthi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 08:48:38 2020

@author: sruthi
"""

import paho.mqtt.client as mqtt


from collections import deque , defaultdict
import matplotlib.animation as animation
from matplotlib import pyplot as plt
import paho.mqtt.client as mqtt
#from plot_data import DataPlot, RealtimePlot
import threading
import json,base64
import matplotlib.pyplot as plt
#import DataPlot and RealtimePlot from the file plot_data.py
#from plot_data import DataPlot, RealtimePlot

class DataPlot:
    def __init__(self, max_entries = 50):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.axis_y2 = deque(maxlen=max_entries)

        self.max_entries = max_entries

        self.buf1=deque(maxlen=5)
        self.buf2=deque(maxlen=5)

     
    def add(self, x, y,y2):

        self.axis_x.append(x)
        self.axis_y.append(y)
        self.axis_y2.append(y2)

class RealtimePlot:
    def __init__(self, axes):
     
        self.axes = axes

        self.lineplot, = axes.plot([], [], "ro-")
        self.lineplot2, = axes.plot([], [], "go-")

    def plot(self, dataPlot):
        self.lineplot.set_data(dataPlot.axis_x, dataPlot.axis_y)
        self.lineplot2.set_data(dataPlot.axis_x, dataPlot.axis_y2)

        self.axes.set_xlim(min(dataPlot.axis_x), max(dataPlot.axis_x))
        ymin = min([min(dataPlot.axis_y), min(dataPlot.axis_y2)])-10
        ymax = max([max(dataPlot.axis_y), max(dataPlot.axis_y2)])+10
        self.axes.set_ylim(ymin,ymax)
        self.axes.relim();


count=0
fig, axes = plt.subplots()
plt.title('Data visualization Evacuation data')

data = DataPlot()
print(data)
dataPlotting= RealtimePlot(axes)


def bytes_to_decimel(i,d):
    xx = i - 127
    dec = (-d if xx < 0 else d)/100
    return xx + dec

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensors/#")
#    client.subscribe("plan")
#    client.subscribe("actuator1")
##    client.subscribe("actuator2")
#message_gas = []
#message_piezo = []
#iter_label=0
#message_gas.append(0)
#message_piezo.append(0)

global message_piezoval

def on_message(client, userdata, msg):
    
    global count
    count+=1
    global message_piezoval 
    
    message =json.loads(msg.payload.decode('UTF-8'))
    message = int(message)
    #int("message")
    
    message_topics = msg.topic
#    message_topics.append(message_topic)
    if message_topics == "sensors/evac/flame":
         message_gasval = message
         
         print(((message_gasval)))
         data.add(count, message_gasval,message_piezoval)
         #message_gas.append(message)
    elif message_topics == "sensors/evac/motion":
        message_piezoval = message
        
        print(((message_piezoval)))
        data.add(count, message_gasval,message_piezoval)

   
    
    dataPlotting.plot(data)
    plt.pause(1)

# set paho.mqtt callback
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.163", 1883, 60) #MQTT port over TLS

try:
    client.loop_forever()
except KeyboardInterrupt:
    print('disconnect')
    client.disconnect()