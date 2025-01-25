import paho.mqtt.client as mqtt
import time

# def on_log(client, userdata, level, buf):
#     print("log: ",buf)

flag_connected = 0
def on_connectN(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   print("Connected with result code "+str(rc))
   client.subscribe("gpio/#")

def on_disconnectN(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("Disconnected with result code "+str(rc))

def on_messageN(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    client.publish("led/504", msg.payload)

clientN = mqtt.Client()
clientN.on_connect = on_connectN
clientN.on_disconnect = on_disconnectN
clientN.on_message = on_messageN
#client.on_log=on_log
clientN.connect("192.168.51.239", 1883, 60)
clientN.loop_start()

#-----------------------------------------------

def on_connectO(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("gpio/#")

# The callback for when a PUBLISH message is received from the server.
def on_messageO(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    client.publish("led/504", msg.payload)

clientO = mqtt.Client()
clientO.on_connect = on_connectO
clientO.on_message = on_messageO
clientO.connect("localhost", 1883, 60)



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
clientO.loop_forever()
