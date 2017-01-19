#include "DHT.h"
#include <Wire.h>
#include "Arduino.h"
#include "SI114X.h"
#define MoisturePin     A1
#define DHTPIN A0     // what pin we're connected to
#define DHTTYPE DHT11   // DHT 11


#define SensorPin A2            //pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00            //deviation compensate
#define LED 13
#define samplingInterval 20
#define printInterval 800
#define ArrayLenth  40    //times of collection
int pHArray[ArrayLenth];   //Store the average value of the sensor feedback
int pHArrayIndex=0;  

DHT dht(DHTPIN, DHTTYPE);
SI114X SI1145 = SI114X();
float airhumidity;
float airtemperature;
int ir;
float ph;
float MoisHumidity;
void setup() {
  // put your setup code here, to run once:
  //Wire.begin();
  Serial.begin(9600); 
  dht.begin();
  while (!SI1145.Begin()) {
    Serial.println("Si1145 is not ready!");
    delay(1000);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  airhumidity = -1;
  airtemperature = -1;
  ir = -1;
  ph = -1;
  MoisHumidity = -1;
  
  airhumidity = readairhumidity();
  Serial.print("airhumidity :");Serial.println(airhumidity);
  delay(1000);
  airtemperature = readairtemperature();
  Serial.print("airtemperature :");Serial.println(airtemperature);
  delay(1000);

  
  ir = readir();
  Serial.print("ir :");Serial.println(ir);
  delay(1000);
  MoisHumidity = readMoisHumidity();
  Serial.print("MoisHumidity :");Serial.println(MoisHumidity);
  delay(1000);
  
  ph = readph();
  Serial.print("ph :");Serial.println(ph);
  delay(1000);
  Serial.println("--------------------------------------");
}

float readph(){
  float ph = -1;
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue,voltage;
  if(millis()-samplingTime > samplingInterval)
  {
      pHArray[pHArrayIndex++]=analogRead(SensorPin);
      if(pHArrayIndex==ArrayLenth)pHArrayIndex=0;
      voltage = avergearray(pHArray, ArrayLenth)*5.0/1024;
      pHValue = 3.5*voltage+Offset;
      samplingTime=millis();
  }
  if(millis() - printTime > printInterval)   //Every 800 milliseconds, print a numerical, convert the state of the LED indicator
  {
/*  Serial.print("Voltage:");
  Serial.print(voltage,2);
  Serial.print("    pH value: ");
  Serial.println(pHValue,2);*/
        
        printTime=millis();
  }
  ph = pHValue;
  return ph;
}

int readir(){
  ir = -1;
  ir = SI1145.ReadIR();
//  Serial.print("IR: "); Serial.println(SI1145.ReadIR());
  return ir;
}

float readairhumidity(){
  float airhumidity = -1;
  
  if (isnan(airhumidity)) 
    {
        airhumidity = -1;
    } 
  airhumidity = dht.readHumidity();
/*  Serial.print("Humidity: "); 
  Serial.print(airhumidity);
  Serial.print(" %\t");*/
  return airhumidity;
}

float readMoisHumidity(){
  int MoisHumidity = -1;
  MoisHumidity = analogRead(MoisturePin)/7 ;
  return MoisHumidity;
  //MoisHumidity   = analogRead(MoisturePin)/7;
//  Serial.println(MoisHumidity);
}

float readairtemperature(){
  float airtemperature = -1;
  
  if (isnan(airtemperature) ) 
    {
        airtemperature = -1;
    } 
  airtemperature = dht.readTemperature();
/*  Serial.print("Temperature: "); 
  Serial.print(airtemperature);
  Serial.println(" *C");*/
  return airtemperature;
}

double avergearray(int* arr, int number){
  int i;
  int max,min;
  double avg;
  long amount=0;
  if(number<=0){
    Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if(number<5){   //less than 5, calculated directly statistics
    for(i=0;i<number;i++){
      amount+=arr[i];
    }
    avg = amount/number;
    return avg;
  }else{
    if(arr[0]<arr[1]){
      min = arr[0];max=arr[1];
    }
    else{
      min=arr[1];max=arr[0];
    }
    for(i=2;i<number;i++){
      if(arr[i]<min){
        amount+=min;        //arr<min
        min=arr[i];
      }else {
        if(arr[i]>max){
          amount+=max;    //arr>max
          max=arr[i];
        }else{
          amount+=arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }//if
  return avg;
}
