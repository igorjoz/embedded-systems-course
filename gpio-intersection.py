from time import *
import RPi.GPIO as GPIO
 
 
sw1 = False
sw2 = False
 
 
def czas():
    GPIO.output(21, 1)
    GPIO.output(21, 0)
 
def setLights(lights):
    setData01()
    for i in range(48):
        if (47 - i) in lights:
            GPIO.output(20, 1)
        else:
            GPIO.output(20, 0)
        czas()
 
    setData10()
def setData01():
    GPIO.output(22, 0)
    GPIO.output(23, 1)
    GPIO.output(24, 1)
    GPIO.output(25, 1)
 
def setData10():
    GPIO.output(22, 1)
    GPIO.output(23, 0)
    GPIO.output(24, 0)
    GPIO.output(25, 0)
 
def stan1():
    def stan11():
        lights = [47, 43, 42, 39, 37, 32, 30, 26, 25, 23, 21, 16, 15, 12, 10, 7, 4, 2]
        setLights(lights)
    def stan12():
        lights = [47, 32, 30, 16, 15, 12, 10, 7, 4, 2]
        setLights(lights)
 
    stan11()
    sleep(3)
    for i in range(4):
        stan12()
        sleep(0.5)
        stan11()
        sleep(0.5)
 
def stan2(switch1State, switch2State):
    def stan21():
        lights = [45, 38, 36, 44, 41, 34, 28, 27, 24, 22, 20, 18, 15, 12, 8, 7, 4, 0]
        setLights(lights)
 
 
    def stan221():
        lights = [45, 38, 36, 44, 41, 34, 28, 27, 24, 22, 20, 18, 14, 13, 8, 7, 4, 0]
        setLights(lights)
 
 
    def stan222():
        lights = [45, 38, 36, 44, 41, 34, 28, 27, 24, 22, 20, 18, 8, 7, 4, 0]
        setLights(lights)
        sleep(0.5)
 
    def stan231():
        lights = [45, 38, 36, 44, 41, 34, 28, 27, 24, 22, 20, 18, 15, 12, 8, 6, 5, 0]
        setLights(lights)
 
    def stan232():
        lights = [45, 38, 36, 44, 41, 34, 28, 27, 24, 22, 20, 18, 15, 12, 8, 0]
        setLights(lights)
 
    def stan241():
        lights = [45, 38, 36, 44, 41, 34, 28, 27, 24, 22, 20, 18, 14, 13, 8, 6, 5, 0]
        setLights(lights)
 
 
    def stan242():
        lights = [45, 38, 36, 44, 41, 34, 28, 27, 24, 22, 20, 18, 8, 0]
        setLights(lights)
 
 
 
    if switch1State and switch2State:
        stan241()
        sleep(2)
        for i in range(2):
            stan242()
            sleep(0.5)
            stan241()
            sleep(0.5)
    elif switch2State:
        stan221()
        sleep(2)
        for i in range(2):
            stan222()
            sleep(0.5)
            stan221()
            sleep(0.5)
    elif switch1State:
        stan231()
        sleep(2)
        for i in range(2):
            stan232()
            sleep(0.5)
            stan231()
            sleep(0.5)
    else:
        stan21()
        sleep(4)
 
 
 
 
 
def stan3():
    lights = [47, 46, 44, 41, 38, 36, 33, 32, 30, 29, 27, 24, 22, 20, 17, 16, 15, 12, 8, 7, 4, 0]
    setLights(lights)
    sleep(1)
 
 
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(26, GPIO.IN)
GPIO.setup(27, GPIO.IN)
 
GPIO.output(21, 0)
 
 
print("before loop")
 
while True:
     # stan1
    stan1()
 
     # stan 2
    if GPIO.input(26) == GPIO.LOW:
        sw1 = True
    if GPIO.input(27) == GPIO.LOW:
        sw2 = True
    stan2(sw1, sw2)
    sw1 = False
    sw2 = False
 
    #stan3
    stan3()