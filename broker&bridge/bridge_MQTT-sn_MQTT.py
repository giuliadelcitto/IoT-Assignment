import json
import time
import os
import paho.mqtt.client as mqtt

#check the connection 
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        
def tb_publish(dev_id, msg):
	#One connecttion per message
	#Broker value 127.0.0.1 if in local, demo.thingsboard.io in livedemo version. Port 1883 for the MQTT connection
	broker="demo.thingsboard.io"
	port=1883
	#topic of the publish is the telemetry of the device (Environment_station1). The id is the device access token
	topic="v1/devices/me/telemetry"
	if dev_id == '1':
		id_client="z5hKTq8bjwvBqGIr5bw3"
	else:
		id_client="0P4MFpOyGlXQKlusWN14"
		
	passwrd=""
		
	mqtt.Client.connected_flag=False
	
	if id_client !="" :
		client = mqtt.Client()
		client.username_pw_set(id_client, passwrd)
	
	#connection and check
	client.connect(broker, port)
	client.on_connect=on_connect
	
	while not client.connected_flag :
		client.loop()
		time.sleep(2)
		
	print("connection finish\n")
	
	client.publish(topic, msg ,0)
	print("data publish ok\n ")
	client.disconnect()
	print("client disconnect\n")
	

def on_message_local(client, userdata, message):
	value = str(message.payload)
	print("data  " + value)
	
	d= value[2:-1]
	data=d.split(",")
	key=["temperature", "humidity", "wind_direction", "wind_intensity", "rain_height"]
	data_out=json.dumps({key[0]:data[1],key[1]:data[2],key[2]:data[3],key[3]:data[4],key[4]:data[5]})
	print("id " + str(data_out))
	
	tb_publish(data[0], data_out)

	
        
def on_connect_local(client, userdata, flags, rc):
	
	print("Connected with result code "+str(rc))
	local_broker.subscribe("sensor/data")  #same of riot topic
	
if __name__ == "__main__":
	
	#create an istance to connect to mqtt-sn broker
	local_broker = mqtt.Client()
	#connect to the mqtt-sn broker
	local_broker.connect('fec0:affe::1',1884,60)
	local_broker.on_connect = on_connect_local
	local_broker.on_message = on_message_local
	local_broker.loop_forever()
    
	print("DONE!")
