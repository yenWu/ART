#include <RCSwitch.h>

#include <EEPROM.h>
#include <RCSwitch.h>

#define RELAY1 4
#define RELAY2 5
#define RELAY3 7

int r1 = 0;
int r2 = 0;
int r3 = 0;

/*RF433*/
int rf433signal = 0;
RCSwitch mySwitch = RCSwitch();

void setup() {

  /*Sprinkler*/
  pinMode(RELAY1,OUTPUT);
  pinMode(RELAY2,OUTPUT);
  pinMode(RELAY3,OUTPUT);
  digitalWrite(RELAY1,LOW); 
  digitalWrite(RELAY2,LOW); 
  digitalWrite(RELAY3,LOW);

  Serial.begin(9600);

  /*RF433*/
  mySwitch.enableReceive(0);
}

void loop(){
  /*Sprinkler*/
  if(r1 == 0)  digitalWrite(RELAY1,LOW); 
  else digitalWrite(RELAY1,HIGH); 
  
  if(r2 == 0)  digitalWrite(RELAY2,LOW); 
  else digitalWrite(RELAY2,HIGH); 
  
  if(r4 == 0)  digitalWrite(RELAY4,LOW); 
  else digitalWrite(RELAY4,HIGH); 
  
  /* RF433 */
  if(rf433signal == 1){
    digitalWrite(RELAY1,LOW); 
    digitalWrite(RELAY2,LOW); 
    digitalWrite(RELAY4,LOW); 
    //Serial.println("get 1 ");
  }
  else if(rf433signal == 2){
    digitalWrite(RELAY1,HIGH);
    digitalWrite(RELAY2,HIGH);
    digitalWrite(RELAY4,HIGH);
    //Serial.println("get 2 ");
  }

  if (mySwitch.available()) {
    
    int value = mySwitch.getReceivedValue();
    
    if (value == 0) {
      /*Serial.print("Unknown encoding");*/
    } else {
      rf433signal = mySwitch.getReceivedValue();
      
      /*Serial.print("Received ");
      Serial.print( mySwitch.getReceivedValue() );
      Serial.print(" / ");
      Serial.print( mySwitch.getReceivedBitlength() );
      Serial.print("bit ");
      Serial.print("Protocol: ");
      Serial.println( mySwitch.getReceivedProtocol() );*/
      
    }

    mySwitch.resetAvailable();
  }
  Serial.print(rf433signal);
  delay(500);
}
