#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import random
import numpy as np
import json

def data_generator():
	data=[0,0,0,0,0]
	#temperature
	data[0]=round(random.uniform(-50, 50),1)
	#humidity
	data[1]=round(random.uniform(0, 100),1)
	#wind direction
	data[2]=random.randint(0, 360)
	#wind intensity
	data[3]=round(random.uniform(0, 100),1)
	#rain height
	data[4]=round(random.uniform(0, 50),1)
	
	return data
	
#check the connection 
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def main(): 
	mqtt.Client.connected_flag=False
	#Broker value 127.0.0.1 if in local, demo.thingsboard.io in livedemo version. Port 1883 for the MQTT connection
	broker="demo.thingsboard.io"
	port=1883
	#topic of the publish is the telemetry of the device (Environment_station1). The id is the device access token
	topic="v1/devices/me/telemetry"
	id_client="z5hKTq8bjwvBqGIr5bw3"
	passwrd=""
	#one key for each sensor
	key=["temperature", "humidity", "wind_direction", "wind_intensity", "rain_height"]
	
	
	if id_client !="" :
		client = mqtt.Client()
		client.username_pw_set(id_client, passwrd)
	
	#connection and check
	client.connect(broker, port)
	client.on_connect=on_connect
	
	while not client.connected_flag :
		client.loop()
		time.sleep(2)
	
	#loop for generation and publishing
	while(1):
		data=data_generator()
		print(data)
		data_out=json.dumps({key[0]:data[0],key[1]:data[1],key[2]:data[2],key[3]:data[3],key[4]:data[4]})
		client.publish(topic, data_out,0);
		time.sleep(2)
	
	client.disconnect();	
	
	
if __name__ == '__main__' : main()
