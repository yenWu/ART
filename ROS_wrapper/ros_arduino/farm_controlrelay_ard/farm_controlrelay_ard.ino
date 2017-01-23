#include <RCSwitch.h>

#include <EEPROM.h>
#include <RCSwitch.h>

/*ROS*/
#include <ros.h>
#include <farm/sprinkler.h>


#define RELAY1 4
#define RELAY2 5
#define RELAY3 7

int r1 = 0;
int r2 = 0;
int r3 = 0;

/*RF433*/
int rf433signal = 0;
RCSwitch mySwitch = RCSwitch();

/*ROS*/
void wrt_spk(const farm::sprinkler &msg)
{
    /*digitalWrite(RELAY1, msg.relay1 == 1? HIGH: LOW);
    digitalWrite(RELAY2, msg.relay2 == 1? HIGH: LOW);
    digitalWrite(RELAY3, msg.relay3 == 1? HIGH: LOW);*/
    r1 = msg.relay1? 1: 0;
    r2 = msg.relay2? 1: 0;
    r3 = msg.relay3? 1: 0;
}

ros::NodeHandle nh;
ros::Subscriber <farm::sprinkler> spk_subr("sprinkler", wrt_spk);

void setup() {

  /*Sprinkler*/
  pinMode(RELAY1,OUTPUT);
  pinMode(RELAY2,OUTPUT);
  pinMode(RELAY3,OUTPUT);
  digitalWrite(RELAY1,LOW); 
  digitalWrite(RELAY2,LOW); 
  digitalWrite(RELAY3,LOW);

  /*ROS*/
  nh.initNode();
  nh.subscribe(spk_subr);
    
  //Serial.begin(9600);

  /*RF433*/
  mySwitch.enableReceive(0);
}

void loop(){
  
  /*Sprinkler*/
  if(r1 == 0)  digitalWrite(RELAY1,LOW); 
  else digitalWrite(RELAY1,HIGH); 
  
  
  if(r2 == 0)  digitalWrite(RELAY2,LOW); 
  else digitalWrite(RELAY2,HIGH); 
  
  if(r3 == 0)  digitalWrite(RELAY3,LOW); 
  else digitalWrite(RELAY3,HIGH); 
  
  /* RF433 */
  if(rf433signal == 1){
    digitalWrite(RELAY1,LOW); 
    digitalWrite(RELAY2,LOW); 
    digitalWrite(RELAY3,LOW); 
    //Serial.println("get 1 ");
  }
  else if(rf433signal == 2){
    digitalWrite(RELAY1,HIGH);
    digitalWrite(RELAY2,HIGH);
    digitalWrite(RELAY3,HIGH);
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
  nh.spinOnce();
  //Serial.print(rf433signal);
  //delay(500);
}
