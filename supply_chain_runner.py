#!/usr/bin/env python


import os
import ConfigParser
from atl_pahomqtt import CarriotsMqttClient
import logging
import serial, time, json, datetime
import atl_utils
from sfdc_utils import SFDCUtils
import RPi.GPIO as GPIO
import thread, time, threading, collections

def post_to_carriots(carriotsMqttClientObject, payload):
	client_mqtt_post = carriotsMqttClientObject 
	logging.debug("posting payload to carriots :%s "  %payload)
	client_mqtt_post.post_to_carriots(payload)
	logging.debug("Posting to carriots complete")

def post_to_salesforce(payload):
	x = SFDCUtils()
	logging.debug("payload for SFDC : %s" %payload)
	resp = x.post(payload)
	logging.info("Post response to SFDC : %s" %resp)
	return resp

def main():
	
	default_cfg = {
		'url'        : 'localhost:1880',
		'baudRate'    : '115200',
		'connectPort'  : '/dev/ttyACM0',
		'device_id'  : '56789'
		}

	cp = ConfigParser.SafeConfigParser(default_cfg)
	cp.read(os.path.splitext(__file__)[0] + '.ini')
	log_file = cp.get('PARAMETERS','log_file')

	logging.basicConfig(filename=log_file,filemode='w', level=logging.DEBUG)

	logging.info('Starting Supply Chain program')
	logging.info('Config read from: ' + os.path.splitext(__file__)[0] + '.ini')

	logging.info('\n==========Started with below configurations========================')
	logging.info('url       : ' + cp.get('PARAMETERS','url'))
	logging.info('baudRate : ' + str(cp.getint('DEVICE_PARAMS','baudRate')))
	logging.info('connectPort  : ' + cp.get('DEVICE_PARAMS','connectPort'))
	logging.info('device_id  : ' + cp.get('DEVICE_PARAMS','device_id'))
	logging.info('post interval : ' +str(cp.getint('PARAMETERS','post_interval')))
	logging.info('\n==================================')
	
	post_interval = cp.getint('PARAMETERS','post_interval')
	uname = cp.get('CARRIOTS_PARAMS','username')
	pwd =  cp.get('CARRIOTS_PARAMS','password')
	auth = {'username': uname, 'password': pwd}
	client_mqtt_post = CarriotsMqttClient(auth)
	start_time = time.time()
	baudRate = cp.getint('DEVICE_PARAMS','baudRate')
	connectPort = cp.get('DEVICE_PARAMS','connectPort')
	device_id = cp.get('DEVICE_PARAMS','device_id')
	
	'''Serial Read from RFID Reader and Accelerometer'''
	ser = serial.Serial(connectPort, baudRate)

	'''Button setup '''
	GPIO.setmode(GPIO.BOARD)
	#12 is button ping 
	GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	#13 is pin for led light
	GPIO.setup(13, GPIO.OUT)
	GPIO.output(13,GPIO.LOW)
	button_press_flag = False
	logging.info("Supply Chain process initiated. Waiting for button press to start polling the data")
	print "File loaded start the process. Happy clicking "
	
 	while True:
 		serial_line = ser.readline()
 		input_state = GPIO.input(12)
 		
 		if input_state == False:
 			button_press_flag = (False if button_press_flag else True)
 			process_status = (" PROCESS STARTED " if button_press_flag else " PROCESS STOPPED ")
 			logging.info("Button Press detected %s as a result of it" %process_status)
 			print ("BUTTON PRESSED. Current flag is %s" %button_press_flag)
			time.sleep(0.2)
		#is button is pressed then glow the light
		if button_press_flag:
			GPIO.output(13,GPIO.HIGH)
		else:
			GPIO.output(13,GPIO.LOW)

		if atl_utils.is_json(serial_line):
 			serial_json = json.loads(serial_line)
 			if "rfid_tag" in serial_json:
				rfid_reading = serial_json
				logging.debug( 'RFID readings: %s' %rfid_reading)
				rfid_tag_id = rfid_reading["rfid_tag"].lstrip('$')
				curr_time = str(datetime.datetime.now().isoformat())
				payload = '{"ID__c":"'+rfid_tag_id+'","SensorID__c":"'+device_id+'","Type__c":"beef","Status__c":"Transit","ShippingTime__c":"'+curr_time+'"}'
				try:
					#thread.start_new_thread( post_to_salesforce, (payload, ) )
					thr = threading.Thread(target=post_to_salesforce,args=(payload,))
					thr.start()
				except Exception, e:
					logging.error("Error while starting a thread to post data to salesforce : %s" %e)
					pass
		
			if button_press_flag and "rfid_tag" not in serial_json:
				elapsed_time = time.time() - start_time
				if elapsed_time >= post_interval:
					payload = serial_json
					logging.debug( 'accelerometer reading: %s' %payload)
					try:
						#thread.start_new_thread( post_to_carriots, (client_mqtt_post,payload, ) )
						nthr = threading.Thread(target=post_to_carriots, args=(client_mqtt_post,payload,))
						nthr.start()
					except Exception, e:
						logging.error("Error while starting a thread to post data to carriots : %s" %e)
						pass
					start_time = time.time()

main()
