#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Client paho-mqtt CarriotsMqttServer
# main.py
import paho.mqtt.publish as publish
import json
from ssl import PROTOCOL_TLSv1
import serial_read_once as read_data
from json import dumps


sensor_id = 'RPi2@Subani.Subani'
class CarriotsMqttClient():
	host = 'mqtt.carriots.com'
	port = '1883'
	auth = {}
	topic = '%s/streams'
	tls = None

	def __init__(self, auth, tls=None):
		self.auth = auth
		self.topic = '%s/streams' % auth['username']
		if tls:
			self.tls = tls
			self.port = '8883'

	def publish(self, msg):
		try:
			publish.single(topic=self.topic, payload=msg, hostname=self.host, auth=self.auth, tls=self.tls, port=self.port)
			print "MQTT message 1:", self.topic, msg, self.host, self.auth, self.tls, self.port
		except Exception, ex:
			print ex


if __name__ == '__main__':
	auth = {'username': 'e60ed329b656fa6d918f058af650a6de26a38b0697b7cf61ab204730cca3a53a', 'password': ''}
    #tls_dict = {'ca_certs': 'ca_certs.crt', 'tls_version': PROTOCOL_TLSv1}  # ssl version
	output_readings = read_data.read_accelerometer()
	print("op read : %s" %output_readings)
	if output_readings:    
		read_json_data = json.loads(output_readings)
		read_json_data['sensor_id'] = sensor_id
		msg_dict = {'protocol': 'v2', 'device': sensor_id, 'at': 'now', 'data': read_json_data}
		client_mqtt = CarriotsMqttClient(auth=auth)                     # non ssl version
		print msg_dict
		client_mqtt.publish(dumps(msg_dict))
    

