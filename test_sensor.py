#import serial

#ser = serial.Serial('/dev/ttyACM0',115200)
#while 1:
#	print ser.readline()

from DHT_ONCE import readDHTsensor
from PIR_ONCE import readPIR


DHT_reading =  readDHTsensor()
print DHT_reading  



PIR_reading = readPIR()
print PIR_reading
