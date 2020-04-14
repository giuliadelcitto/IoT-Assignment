import paho.mqtt.client as mqtt
import json 
import time
#check the connection 
def on_connect(client, userdata, flags, rc):
	print("in on connect tb")
	if rc==0:
		client.connected_flag=True #set flag
		print("connected OK")
	else:
		print("Bad connection Returned code=",rc)

def tb_send(dev_id, dev_msg):
	#One connecttion per message
	#Broker value 127.0.0.1 if in local, demo.thingsboard.io in livedemo version. Port 1883 for the MQTT connection
	broker="demo.thingsboard.io"
	port=1883
	#topic of the publish is the telemetry of the device (Environment_station1). The id is the device access token
	topic="v1/devices/me/telemetry"
	
	if (dev_id=="environmental_station_1"):
		id_client="z5hKTq8bjwvBqGIr5bw3"
		print("connect to 1\n")
	else:
		id_client="0P4MFpOyGlXQKlusWN14"
		print("connect to 2\n")
	passwrd=""
		
	mqtt.Client.connected_flag=False
	
	if id_client !="" :
		client = mqtt.Client()
		client.username_pw_set(id_client, passwrd)
	
	print("id_client OK\n")
	
	#connection and check
	client.connect(broker, port)
	print("post client.connect")
	client.on_connect=on_connect
	
	while not client.connected_flag :
		client.loop()
		time.sleep(2)
		
	print("connection finish\n")
	
	client.publish(topic, dev_msg ,0)
	print("data publish ok\n ")
	client.disconnect()
	print("client disconnect\n")

def on_connect_ttn(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("+/devices/+/up")
    print("subscribe ok")
	
# The callback for when a PUBLISH message is received from the server.
def on_message_ttn(client, userdata, msg):
	msg=msg.payload
	print(msg)
	print("\n---------->FINE PAYLOAD\n")
	#json become dictionary
	json_data=json.loads(msg)
	print("ok json.load\n")
	
	device_id=json_data["dev_id"]
	msg_payload=json_data["payload_fields"]["msg"]
	
	data=msg_payload.split(",")
	
	key=["temperature", "humidity", "wind_direction", "wind_intensity", "rain_height"]
	
	data_out=json.dumps({key[0]:data[0],key[1]:data[1],key[2]:data[2],key[3]:data[3],key[4]:data[4]})
		
	print(data_out)
	tb_send(device_id, data_out)
	


client = mqtt.Client()
client.on_connect = on_connect_ttn
client.on_message = on_message_ttn
client.username_pw_set("stations_application", "ttn-account-v2.Gt2pdnIJjHIbbjfrAVsI5-41mCW9Hk39wyuwUTeK-cI" )
client.connect("eu.thethings.network", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
