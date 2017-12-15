# IMPORTS
import sys
import time
import random
import paho.mqtt.client as mqtt
from grovepi import *
from grove_rgb_lcd import *

# OUTPUT
# Grove Red LED to digital port D4
RED_LED = 4
LEDIsOff = True # Flag

def toggleLED():
    if LEDIsOff:
        digitalWrite(RED_LED, 1)
        global LEDIsOff
        LEDIsOff = False
    else:
        digitalWrite(RED_LED, 0)
        global LEDIsOff
        LEDIsOff = True

pinMode(RED_LED, "OUTPUT")
time.sleep(1)

# MQTT CLIENT CONFIG
mqttc = mqtt.Client()

def on_message(client, userdata, msg):
#    if msg.topic == "ASatija/Ultrasonic":
#        sensors['Ultrasonic'] = msg.payload
#    elif msg.topic == "ASatija/Sound":
#        sensors['Sound'] = msg.payload
#    elif msg.topic == "ASatija/Rotary":
#        sensors['Rotary'] = msg.payload
#    elif msg.topic == "ASatija/Light":
#        sensors['Light'] = msg.payload
#    elif msg.topic == "ASatija/Red_LED":
#        toggleLED()
    key = msg.topic[8:]
    value = msg.payload
    setRGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    setText(key + ": \n" + str(value))

mqttc.on_message = on_message
mqttc.username_pw_set("Your IOT Cloud Username", password="Your IOT cloud password")
mqttc.connect("Your Cloud Server's IP address", Port Number goes here)
mqttc.subscribe([("ASatija/Ultrasonic", 1), ("ASatija/Sound", 1), ("ASatija/Rotary", 1), ("ASatija/Light", 1),
                 ("ASatija/Red_LED", 1)])

mqttc.loop_start()

while True:
    try:
        time.sleep(.9)

    except KeyboardInterrupt:
        switch.disconnect()
        mqttc.disconnect()
        switch.loop_stop()
        mqttc.loop_stop()
        digitalWrite(RED_LED, 0)
        setText("Subscriber dead \n:(")
        setRGB(255, 0, 0)
        time.sleep(1)
        sys.exit()
    except IOError:
        print "Error" 
