#include <ros.h>
#include <dht.h>   
#include <farm/dht0.h>

ros::NodeHandle  nh;

farm::dht0 dht0;
ros::Publisher pub_dht0("Arduino_dht0", &dht0);

#define dht_dpin 2 //定義訊號要從Pin A0 進來  
  
dht DHT;

void wrt_dht(farm::dht &msg, dht d)
{
	msg.humid = d.humidity;
	msg.temp = d.temperature;
}
  
void setup(){   
	Serial.begin(9600);   
	delay(300);             //Let system settle   
	//Serial.println("Humidity and temperature\n\n");   
	delay(700);             //Wait rest of 1000ms recommended delay before   
	//accessing sensor   
	nh.initNode();
	nh.subscribe(subard);
}
  
void loop(){
	DHT.read11(dht_dpin);   //去library裡面找DHT.read11
	wrt_dht(dht0, DHT);
	pub_dhp.publish(&dht0_msg);

	/*Serial.print("Humidity = ");   
	Serial.print(DHT.humidity);   
	Serial.print("% ");   
	Serial.print("temperature = ");   
	Serial.print(DHT.temperature);   
	Serial.println("C ");*/

	nh.spinOnce();

	delay(1000);            //每1000ms更新一次   
}  


