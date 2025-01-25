import paho.mqtt.client as mqtt
import gpio
# The callback for when the client receives a CONNACK response from the server.

gpio.setup(504, gpio.OUT)

def on_connect1(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors/bme280/#")

# The callback for when a PUBLISH message is received from the server.
def on_message1(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if int(msg.payload) >= 28:
        client1.publish("led/504", "1")
    if int(msg.payload) < 28:
        client1.publish("led/504", "0")


client1 = mqtt.Client()
client1.on_connect = on_connect1
client1.on_message = on_message1
client1.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client1.loop_start()

#---------------------------------


def on_connect2(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors/bme280/#")

# The callback for when a PUBLISH message is received from the server.
def on_message2(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if int(msg.payload) >= 28:
        client1.publish("led/504", "1")
    if int(msg.payload) < 28:
        client1.publish("led/504", "0")


client2 = mqtt.Client()
client2.on_connect = on_connect2
client2.on_message = on_message2
client2.connect("192.168.51.239", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client2.loop_forever()