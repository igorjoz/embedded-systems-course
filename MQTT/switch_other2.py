import paho.mqtt.client as mqtt
import time

# def on_log(client, userdata, level, buf):
#     print("log: ",buf)

flag_connected = 0
def on_connect1(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   print("Connected with result code "+str(rc))
   client.subscribe("gpio/#")

def on_disconnect1(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("Disconnected with result code "+str(rc))

def on_message1(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    client2.publish("led/504", msg.payload)

client1 = mqtt.Client()
client1.on_connect = on_connect1
client1.on_disconnect = on_disconnect1
client1.on_message = on_message1
#client.on_log=on_log
client1.connect("192.168.51.239", 1883, 60)
client1.loop_start()

#-----------------------------------------------

def on_connect2(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("gpio/#")

# The callback for when a PUBLISH message is received from the server.
def on_message2(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    client1.publish("led/504", msg.payload)

client2 = mqtt.Client()
client2.on_connect = on_connect2
client2.on_message = on_message2
client2.connect("localhost", 1883, 60)



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client2.loop_forever()
