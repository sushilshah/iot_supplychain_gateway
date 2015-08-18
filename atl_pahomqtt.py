#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Client paho-mqtt CarriotsMqttServer
# main.py
import paho.mqtt.publish as publish
from json import dumps
from ssl import PROTOCOL_TLSv1
import json, logging
from PIR_ONCE import readPIR
from DHT_ONCE import readDHTsensor
from uuid import getnode as get_mac
import atl_utils
 

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
			#print "MQTT message published:", self.topic, msg, self.host, self.auth, self.tls, self.port
			logging.info( "MQTT message published: " + msg)
		except Exception, ex:
			logging.error(ex)

	def post_to_carriots(self, additional_payload):
	#	auth = {'username': 'e60ed329b656fa6d918f058af650a6de26a38b0697b7cf61ab204730cca3a53a', 'password': ''}

		DHT_reading =  readDHTsensor()
		PIR_reading = readPIR()
		mac_address = get_mac()
		data_string = '{ "sensor_id" : "' + str(mac_address) +'",'  +  DHT_reading + ", " + PIR_reading + '}'
#		logging.debug("data String %s " %data_string )
		data_json = json.loads(data_string)
		merged_json = atl_utils.merge_json(data_json, additional_payload)
		logging.debug("posting data to carriots")
		logging.debug(merged_json)
	#	msg_dict = {'protocol': 'v2', 'device': 'defaultDevice@Subani.Subani', 'at': 'now', 'data': {'temp': 24, 'hum':58}}
		msg_dict = {'protocol': 'v2', 'device': 'defaultDevice@Subani.Subani', 'at': 'now', 'data': merged_json}
		#client_mqtt = CarriotsMqttClient(auth=auth)                     # non ssl version
		#client_mqtt.publish(dumps(msg_dict))
		self.publish(dumps(msg_dict))


if __name__ == '__main__':
	auth = {'username': 'e60ed329b656fa6d918f058af650a6de26a38b0697b7cf61ab204730cca3a53a', 'password': ''}
	client_mqtt_post = CarriotsMqttClient(auth)  
	client_mqtt_post.post_to_carriots()
