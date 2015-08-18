import serial
#http://blog.oscarliang.net/connect-raspberry-pi-and-arduino-usb-cable/
import json

def json_parse(text):
	        try:
       #        return json.loads(text)
			json.loads(text)
			return True
		except ValueError as e:
		#	print('invalid json: %s' % e)
			return False # or: raise






ser = serial.Serial('/dev/ttyACM0', 115200)
#while 1 :
	#readString = ser.readline()
	#print "Hello World"
	#print readString

try:
	readString = ser.readline().strip()
#	print ('readString: %s' %readString)
	if not readString:
		pass #read empty string. ignoring it
	else:
		if json_parse(readString):
			print readString


except:
	pass



