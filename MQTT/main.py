#!/usr/bin/env python3.6
import time
import gpio
print( "Test LED@PWM0\n")
gpio.setup(504, gpio.OUT)

gpio.setup(488, gpio.IN)

isOn = False
gpio.set(504, 0)
time.sleep(0.5)

# gpio.log.setLevel(logging.INFO)
while(True):
    if isOn != gpio.read(488):
        isOn = not isOn
        print(isOn)
        gpio.set(504, isOn)
    time.sleep(0.5)
    