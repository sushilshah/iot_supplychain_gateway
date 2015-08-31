
#include <PinChangeInt.h>
#include <eHealth.h>
#include <QueueArray.h>
#include <Time.h>

int cont = 0;
float f_temperature = 0;
int i_prbpm = 0;
int i_spo2 = 0;
uint8_t body_position = 0; 
int i_systolic = 0;
int i_diastolic = 0;
int READINGS_PRINT_TIME_INTERVAL = 1; //ONE SEC

boolean zero_reading_flag = 1;
time_t start_time_rr;
int elapsed_time = 0;
int REFRESH_TIME_INTERVAL = 30; //30 secs
float respiration_rate_per_min = 0.0;
QueueArray <time_t> queue;

time_t start_time;

void setup() {
  
  //eHealth.readBloodPressureSensor();
  //Serial.begin(19200);  
  Serial.begin(115200);  
  eHealth.initPulsioximeter();
  queue.setPrinter(Serial);
  //eHealth.initPositionSensor(); 
  //Attach the inttruptions for using the pulsioximeter.   
  PCintPort::attachInterrupt(6, readPulsioximeter, RISING);

  start_time = now();
}

void loop() {

  if(now() - start_time >= READINGS_PRINT_TIME_INTERVAL){
    serialStreamPulsioximeter();
    readTemperature();
    //readBodyPosition();
    readBloodPressure();
    
    printSensorReadings();
    start_time = now();  
  }
  //This is analogue singal, keep on reading without wait. 
  respiratoryRateReading();
  //int air = eHealth.getAirFlow();   
  //delay(1000);  // wait for a second

}


//Include always this code when using the pulsioximeter sensor
//=========================================================================
void readPulsioximeter(){  
  cont ++;
  if (cont == 50) { //Get only of one 50 measures to reduce the latency
    eHealth.readPulsioximeter();  
    cont = 0;
  }
}


void readTemperature(){
  f_temperature = eHealth.getTemperature();
}

void readBodyPosition(){
  body_position = eHealth.getBodyPosition(); 
}


void serialStreamPulsioximeter(){
  i_prbpm =  eHealth.getBPM();
  i_spo2 = eHealth.getOxygenSaturation();
}

void readBloodPressure(){
 
     eHealth.readBloodPressureSensor();
     Serial.begin(115200);
   
    uint8_t numberOfData = eHealth.getBloodPressureLength(); 
    if(numberOfData > 0){
          //Just use the last readings 
      i_systolic = 30 + eHealth.bloodPressureDataVector[numberOfData -1 ].systolic;
      i_diastolic = eHealth.bloodPressureDataVector[numberOfData - 1].diastolic;
    }else{
      i_systolic  = 0;
      i_diastolic = 0;
    } 
}

void respiratoryRateReading(){
  int air = eHealth.getAirFlow();
  
  if(queue.isEmpty()){
    start_time_rr = now();
    elapsed_time = now() - start_time_rr;
  }else{
    elapsed_time = now() - queue.peek() ;
  }
      
  if(air > 10 && zero_reading_flag == 1 ){
    zero_reading_flag = 0;
    queue.push(now());
    if(elapsed_time <= 0)
      elapsed_time = 1; //TO Avoid INF as count/0 is INFINITY
    respiration_rate_per_min = ((float)queue.count() / (float)elapsed_time) * 60;
  }
  
  if(air == 0)
    zero_reading_flag = 1;
  
  if(elapsed_time >= REFRESH_TIME_INTERVAL){
    while(!queue.isEmpty() && (now() - queue.peek() >= REFRESH_TIME_INTERVAL))
      queue.pop();
    if(queue.isEmpty())
       respiration_rate_per_min = 0;
  }
}

void printSensorReadings(){
  //String outputString = "";
  char temp[10] = {0};
 dtostrf(f_temperature, 1, 2,temp );
 String tempAsString =  String(temp);
// outputString = "{ \"Temperature\" : " + tempAsString + ", \"prbpm\": " + String(i_prbpm) + ", \"spo2\": " + String(i_spo2) + ", \"bodyposition\": " + String(body_position) + " }";
//"temperature":98,"pulse":126,"respiratoryRate":18,"systolic":91,"diastolic":71
String outputString  = "{ \"temperature\" : " + tempAsString + ", \"pulse\": " + String(i_prbpm) + ", \"systolic\":"+String(i_systolic)+",\"diastolic\":"+String(i_diastolic)+ ", \"respiratoryRate\":"+respiration_rate_per_min+" }";
Serial.println(outputString);
}
