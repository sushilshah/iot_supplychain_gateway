#!/usr/bin/env python
#Author: Sushil Shah

import os
import ConfigParser
import logging
import serial, time, json
import atl_utils
import subprocess
import urllib
import urllib2


class SFDCUtils:
	def generate_token(self):
		logging.debug('Config read from: ' + os.path.splitext(__file__)[0] + '.ini')
		default_cfg = {}
		cp = ConfigParser.SafeConfigParser(default_cfg)
		cp.read(os.path.splitext(__file__)[0] + '.ini')

		logging.debug('\n==================================')
		logging.debug('url       : ' + cp.get('PARAMETERS','url'))
		client_id = cp.get('SFDC_PARAMS','client_id')
		client_secret =  cp.get('SFDC_PARAMS','client_secret')
		username = cp.get('SFDC_PARAMS','username')
	 	password = cp.get('SFDC_PARAMS','password')
		url = cp.get('SFDC_PARAMS','url')
		values = {"grant_type":"password",
			"client_id":client_id,"client_secret":client_secret,"username":username,"password":password}
		logging.info("Contacting server to get new token")
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		resp = response.read()
		
		resp_json = json.loads(resp)
		if 'access_token' in resp_json:
			logging.info("Successfully fetched token from server")
			access_token = 'Authorization:Bearer ' +  resp_json['access_token']
			return access_token
		else:
			logging.error("Unhandles operation. Received response is : %s" %resp )
			return None
			


	def post_to_sfdc(self, payload, url, authorization_bearer_header):
		resp = subprocess.check_output(['curl', '-H', "Content-Type:application/json",'-X','POST', '--data',payload,'-H',authorization_bearer_header,url])
		return resp

	def post(self, payload):
		default_cfg = {
			}
		config_file =  os.path.splitext(__file__)[0] + '.ini'
		logging.debug('Config read from: ' + config_file)
		cp = ConfigParser.SafeConfigParser(default_cfg)
		cp.read(config_file)

		logging.debug('\n==================================')
		logging.debug('url       : ' + cp.get('PARAMETERS','url'))
		authToken = cp.get('PARAMETERS', 'authorization_bearer_header')
		url = cp.get('PARAMETERS','url')
		resp = self.post_to_sfdc(payload, url, authToken)
		response_json = json.loads(resp)
		if 'success' in response_json and response_json['success'] == True:
			logging.debug("Posting data success. Response json : %s " %resp)
		elif len(response_json) == 1 and response_json[0]['errorCode'] == 'INVALID_SESSION_ID':
			logging.warning("Session expired. Re-fetching Session token")
			authToken = self.generate_token()
			if authToken :
				cp.set('PARAMETERS','authorization_bearer_header',authToken )
				cp.set('PARAMETERS', 'authorization_bearer_header', authToken)
				with open (config_file, 'w') as configfile:
					cp.write(configfile)
				logging.debug("New auth token updated in config file")
				resp = self.post_to_sfdc(payload, url, authToken)
				logging.info("Reposting data to server. Response received is : %s" %resp)
		else:
			logging.error("Unhandled error. Response json : ")
			logging.error(resp)
		return resp

	

