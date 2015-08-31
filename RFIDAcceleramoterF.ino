
#include <SoftwareSerial.h>

SoftwareSerial mySerial(9, 10);
char data_temp, RFID_data[12];
int read_count=0;

//Accelerometer
const int groundpin = 18;             // analog input pin 4 -- ground
const int powerpin = 19;              // analog input pin 5 -- voltage
const int xpin = A3;                  // x-axis of the accelerometer
const int ypin = A2;                  // y-axis
const int zpin = A1;                  // z-axis (only on 3-axis models)
String accelerometerReading = "";

void setup()
{
  mySerial.begin(9600); // Setting the baud rate of Software Serial Library  
  Serial.begin(9600);  //Setting the baud rate of Serial Monitor 

  // Provide ground and power by using the analog inputs as normal
  // digital pins.  This makes it possible to directly connect the
  // breakout board to the Arduino.  If you use the normal 5V and
  // GND pins on the Arduino, you can remove these lines.
  pinMode(groundpin, OUTPUT);
  pinMode(powerpin, OUTPUT);
  digitalWrite(groundpin, LOW); 
  digitalWrite(powerpin, HIGH);
 }
void loop()
{

  char* foo = RecieveData();
  if(String(foo[0]) == "$"){
    Serial.println("{ \"rfid_tag\" : \"" + String(foo) + "\"}");
  }

  accelerometerReading = "";
  // print the sensor values:
  accelerometerReading += "\"x-axis\": " + String(analogRead(xpin)) + ",";
  accelerometerReading += "\"y-axis\": " + String(analogRead(ypin)) + ",";
  accelerometerReading += "\"z-axis\": " + String(analogRead(zpin));
  
  Serial.println("{" + accelerometerReading + "}");
  delay(1000);
}

char* RecieveData()
{
  char* empty ="";
  if(mySerial.available()>0){
    while(read_count<=10) {  
      data_temp=mySerial.read();
      RFID_data[read_count]=data_temp;
      read_count++;
    }
    if(read_count >= 10) {              // if 10 digit read is complete 
      read_count = 0;
      return RFID_data;// print the TAG code 
    } 
    read_count = 0;
  }
  return empty;
}

