#!/usr/bin/env python


import os
import ConfigParser
import logging
import serial, time, json
import atl_utils
import subprocess

class SFDCUtils:
	def generate_token():
		print "Implement this code"
	
 	
	def post_to_sfdc(self, payload, url, authorization_bearer_header):
		resp = subprocess.check_output(['curl', '-H', "Content-Type:application/json",'-X','POST', '--data',payload,'-H',authorization_bearer_header,url])
		return resp

	def post(self, payload):
		default_cfg = {
			}
		print('Config read from: ' + os.path.splitext(__file__)[0] + '.ini')
		cp = ConfigParser.SafeConfigParser(default_cfg)
		cp.read(os.path.splitext(__file__)[0] + '.ini')

		print('\n==================================')
		print('url       : ' + cp.get('PARAMETERS','url'))
		authToken = cp.get('PARAMETERS', 'authorization_bearer_header')
		url = cp.get('PARAMETERS','url')
		return self.post_to_sfdc(payload, url, authToken)
	
	
