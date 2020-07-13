import RPi.GPIO as GPIO
import time
import paho.mqtt.client as MQTT
import os

client = MQTT.Client(client_id='publisher_flame_motion')
client.connect("127.0.0.1",1883)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
servoPIN = 13
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz


FLAME_SENSOR_PIN = 40
PIR_SENSOR_PIN = 11
GPIO.setup(FLAME_SENSOR_PIN, GPIO.IN)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)

LED_PIN=13
GPIO.setup(LED_PIN, GPIO.OUT)#LED output pin
GPIO.output(LED_PIN, 0)

def my_callback_Motion(channel):
    if(GPIO.input(PIR_SENSOR_PIN)):
        client.publish("sensors/evac/motion",1)
        GPIO.output(LED_PIN,1)
        print("Motion Detected")
        p.start(2.5)
        p.ChangeDutyCycle(3)
        time.sleep(0.5)
        p.ChangeDutyCycle(0)
        time.sleep(0.5)
        p.ChangeDutyCycle(0.5)
        time.sleep(0.5)
        p.stop()
        time.sleep(1)
        GPIO.output(LED_PIN,0)
    else:
        GPIO.output(LED_PIN,0)
        client.publish("sensors/evac/motion",0)
        print("Not Detected")

def my_callback_Flame(channel):

    if not(GPIO.input(FLAME_SENSOR_PIN)):

        #os.system("cd /home/pi/Desktop")
        #os.system("python3 led_blink_buzzer.py")
        GPIO.output(8, GPIO.HIGH)
        GPIO.output(3, GPIO.HIGH)
        client.publish("sensors/evac/flame",1)
        print('Flame Detection')
        time.sleep(1)

    else:
        client.publish("sensors/evac/flame",0)
        print("Flame not detected")




try:
    GPIO.add_event_detect(FLAME_SENSOR_PIN,GPIO.RISING, callback= my_callback_Flame)
    GPIO.add_event_detect(PIR_SENSOR_PIN,GPIO.RISING, callback= my_callback_Motion)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.output(8, GPIO.LOW)
    GPIO.output(3, GPIO.LOW)
    GPIO.cleanup()
    print("Keyboard Interrupt detected, ;)")



GPIO.cleanup()
client.loop()