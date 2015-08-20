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

class SerialReadThread(threading.Thread):
	rfid_queue = collections.deque(5*[""], 5)
	def __init__(self,connectPort,baudRate):
		super(SerialReadThread, self).__init__()
		self.connectPort=connectPort
		self.baudRate=baudRate
		self.total = 0

	def run(self):
		ser = serial.Serial(self.connectPort, self.baudRate)
		while True:
			serial_line = ser.readline()
			print ("Connection port %s" %self.connectPort)
			print serial_line
#			time.sleep(3)
			
			self.rfid_queue.append(time.time())
			print  ("baudrate : %s" %self.baudRate)
			if atl_utils.is_json(serial_line):
				serial_json = json.loads(serial_line)
				if "rfid_tag" in serial_json:
					print "rfid read "
					print serial_line



def post_to_carriots(carriotsMqttClientObject, payload):
	client_mqtt_post = carriotsMqttClientObject 
	#client_mqtt_post.post_to_carriots(payload)
	print "sleep carriots"
	time.sleep(5)

def post_to_salesforce(payload):
	x = SFDCUtils()
	print "sleep salesforce"
	time.sleep(5)
	logging.debug("payload : %s" %payload)
	#resp = x.post(payload)
	#logging.info("Post response : %s" %resp)

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

	logging.basicConfig(filename=log_file,filemode='w', level=logging.INFO)

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
	GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	button_press_flag = False
	logging.info("Supply Chain process initiated. Waiting for button press to start polling the data")
	print "FIle loaded start the process. Happy clicking "
	t = SerialReadThread(connectPort, baudRate)
        t.start()
	
 	while True:
 		input_state = GPIO.input(12)
 		if input_state == False:
 			button_press_flag = (False if button_press_flag else True)
 			process_status = (" PROCESS STARTED " if button_press_flag else " PROCESS STOPPED ")
 			logging.info("Button Press detected %s as a result of it" %process_status)
 			print ("BUTTON PRESSED. Current flag is %s" %button_press_flag)
			time.sleep(0.2)
# 		serial_line = ser.readline()
# 		if atl_utils.is_json(serial_line):
# 			serial_json = json.loads(serial_line)
# 			if "rfid_tag" not in serial_json and button_press_flag:
# 				logging.debug( 'accelerometer reading: %s' %serial_line)
# 				elapsed_time = time.time() - start_time
# 				if elapsed_time >= post_interval:
# 					#client_mqtt_post.post_to_carriots(serial_json)
# 					try:
# 						thread.start_new_thread( post_to_carriots, (client_mqtt_post,serial_json, ) )
# 					except Exception, e:
# 						logging.error("Error while starting a thread to post data to carriots : %s" %e)
# 						pass
# 					start_time = time.time()
# 			elif "rfid_tag" in serial_json:
# 				print serial_line
# 				logging.debug( 'RFID readings: %s' %serial_line)
# 				rfid_tag_id = serial_json["rfid_tag"].lstrip('$')
# 				curr_time = str(datetime.datetime.now().isoformat())
# 				#x = SFDCUtils()
# 				payload = '{"ID__c":"'+rfid_tag_id+'","SensorID__c":"'+device_id+'","Type__c":"beef","Status__c":"Transit","ShippingTime__c":"'+curr_time+'"}'
# 				#logging.debug("payload : %s" %payload)
# 				#resp = x.post(payload)
# 				try:
# 					thread.start_new_thread( post_to_salesforce, (payload, ) )
# 				except Exception, e:
# 					logging.error("Error while starting a thread to post data to salesforce : %s" %e)
# 					pass
#				


main()
