import paho.mqtt.client as mqtt
import time
import gpio

# def on_log(client, userdata, level, buf):
#     print("log: ",buf)

gpio.setup(488, gpio.IN)

flag_connected = 0
def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   print("Connected with result code "+str(rc))

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("Disconnected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_log=on_log
client.connect("localhost", 1883, 60)
client.loop_start()

while(True):
    if flag_connected == 1:
        # Publish message
        client.publish("gpio/488", gpio.read(488))
        time.sleep(1)
        # client.publish("led/504", "0")
        # time.sleep(1)
    else:
        # Wait to reconnect
        time.sleep(5)
        client.reconnect()