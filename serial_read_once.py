import serial, time
from atl_py_lib import is_json

def read_accelerometer():
	ser = serial.Serial('/dev/ttyACM0', 9600)
	try:
		serial_line = ser.readline()
		if is_json(serial_line):
			return serial_line.strip() # print only if correct json format have been received.
	except:
		pass #Bad but i dont want to print anything
# Do some other work on the data

#    time.sleep(300) # sleep 5 minutes

    # Loop restarts once the sleep is finished

#ser.close() # Only executes once the loop exits 
if __name__ == '__main__':
	print read_accelerometer()
	

