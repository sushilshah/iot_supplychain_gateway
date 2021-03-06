#!/usr/bin/env python
#Library of General Utils
#Author: Sushil Shah

import json

def is_json(myjson):
	try:
		json_object = json.loads(myjson)
  	except ValueError, e:
  		return False
	return True
'''Accepts JSON as input params'''
def merge_json(json1, json2):
	merged_json = dict(json1.items() + json2.items())
	return merged_json

def merge_json_str(jsonStr1, jsonStr2):
	if is_json(jsonStr1) and is_json(jsonStr2):
		json1 = json.loads(jsonStr1)
		json2 = json.loads(jsonStr2)
		return merge_json(json1, json2)
	else:
		print "Incorrect json"
