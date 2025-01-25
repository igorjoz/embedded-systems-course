
#!/usr/bin/env python3.6

import paho.mqtt.client as mqtt
import time


path_temp = "/sys/bus/iio/devices/iio:device0/in_temp_input"
path_pres = "/sys/bus/iio/devices/iio:device0/in_pressure_input"
path_hum = "/sys/bus/iio/devices/iio:device0/in_humidityrelative_input"

isOn = False

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
    global isOn
    if isOn == False and int(msg.payload) == True:
        isOn = not isOn
        with open(path_temp,'r',encoding = 'utf-8') as f:
            client1.publish("sensors/bme280/temp", f.read())
        print(isOn)
    elif isOn != int(msg.payload):
        isOn = not isOn



client1 = mqtt.Client()
client1.on_connect = on_connect1
client1.on_disconnect = on_disconnect1
client1.on_message = on_message1
#client.on_log=on_log
client1.connect("localhost", 1883, 60)
client1.loop_start()

while(True):
    '''
    time.sleep(5)
    
    with open(path_temp,'r',encoding = 'utf-8') as f:
        client1.publish("sensors/bme280/temp", f.read())
    with open(path_pres,'r',encoding = 'utf-8') as f:
        client1.publish("sensors/bme280/pres", f.read())
    with open(path_hum,'r',encoding = 'utf-8') as f:
        client1.publish("sensors/bme280/hum", f.read())
    '''


