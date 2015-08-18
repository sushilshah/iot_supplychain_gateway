#!/usr/bin/python
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
PIN_NO = 11
GPIO.setup(PIN_NO, GPIO.IN)         #Read output from PIR motion sensor
#GPIO.setup(3, GPIO.OUT)         #LED output pin
def readPIR():
	i=GPIO.input(PIN_NO)

	if i==0:                 #When output from motion sensor is LOW
		return '"Motion_detected":0'
             #GPIO.output(3, 0)  #Turn OFF LED
        #	time.sleep(0.1)
	elif i==1:               #When output from motion sensor is HIGH
		return '"Motion_detected":1'
             #GPIO.output(3, 1)  #Turn ON LED
	 #       time.sleep(0.1)


if __name__ == '__main__':
	print readPIR()
