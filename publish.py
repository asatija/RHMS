# IMPORTS
import json
import sys
import time
import requests
import paho.mqtt.client as mqtt
from grovepi import *

# SENSORS
# Grove UltraSonic Sensor to digital port D8
ULTRASON = 8
# Grove Sound Sensor to analog port A0
SOUND = 0
# Grove Rotary Angle Sensor to analog port A1
ROTARY = 1
# Grove Light Sensor to analog port A2
LIGHT = 2


# SET PINMODES
pinMode(SOUND, "INPUT")
pinMode(ROTARY, "INPUT")
pinMode(LIGHT, "INPUT")
time.sleep(1)

# VARIABLES
# SOUND SENSOR: The threshold to activate 400.00 * 5 / 1024 = 1.95v
Sound_threshold = 150
# LIGHT SENSOR: The threshold to cross
Light_threshold = 10

# MQTT CLIENT CONFIG
mqttc = mqtt.Client()
mqttc.username_pw_set("user18", password="tmv7ZRZ7")
mqttc.connect("202.50.209.80", 1883)
mqttc.loop_start()

while True:
    try:
        time.sleep(1)

        # Read the ultrasonic sensor value
        Ultrasonic = ultrasonicRead(ULTRASON)
        mqttc.publish("ASatija/Ultrasonic", Ultrasonic)

        time.sleep(1)

        # Read the sound level
        Sound = analogRead(SOUND)
        # If louder than threshold, publish value to broker
        if Sound > Sound_threshold:
            mqttc.publish("ASatija/Sound", Sound)

        time.sleep(1)

        # Read rotary angle value
        Rotary = analogRead(ROTARY)
        mqttc.publish("ASatija/Rotary", Rotary)

        time.sleep(1)

        # Get light sensor value
        Light = analogRead(LIGHT)
        # Calculate resistance of sensor in K
        resistance = (float)(1023 - Light) * 10 / Light
        if resistance > Light_threshold:
            mqttc.publish("ASatija/Light", Light)

        time.sleep(1)

        payload = {
            'Ultrasonic': Ultrasonic,
            'Sound': Sound,
            'Rotary': Rotary,
            'Light': Light
        }
        req = requests.post("https://dweet.io/dweet/for/ankur-satija", data = payload)
        
        
    except KeyboardInterrupt:
        mqttc.disconnect()
        mqttc.loop_stop()
        time.sleep(1)
        sys.exit()
    except TypeError:
        print "TypeError"
        mqttc.disconnect()
        mqttc.loop_stop()
    except IOError:
        print "I/O Error"
        mqttc.disconnect()
        mqttc.loop_stop()
 
