#!/usr/bin/env python


import os
import ConfigParser
from atl_pahomqtt import CarriotsMqttClient
import logging
import serial, time, json
import atl_utils

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

	'''Serial Read from RFID Reader and Accelerometer'''
	ser = serial.Serial(connectPort, baudRate)
	while 1:
		serial_line = ser.readline()
		if atl_utils.is_json(serial_line):
			logging.debug(serial_line)
			serial_json = json.loads(serial_line)
			if "rfid_tag" not in serial_json:
				logging.info( 'accelerometer reading')
				elapsed_time = time.time() - start_time
				if elapsed_time >= post_interval:
					client_mqtt_post.post_to_carriots(serial_json)
					start_time = time.time()
			else:
				logging.info( 'RFID readings')
				logging.info( serial_json)


main()
