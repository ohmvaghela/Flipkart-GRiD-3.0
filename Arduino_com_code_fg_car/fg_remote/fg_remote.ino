#include <SPI.h>
#include <RF24.h>

RF24 radio(7,8);
const byte address[6] = "00001";

String dummy;
int message[7]={1,1,1,1,1,1,1};

void setup() {
  
  Serial.begin(9600);
  radio.begin();
  //Serial.println("checking if chip connected");
  bool check = radio.isChipConnected();
  //Serial.print("check-");
  //Serial.println(check);
  
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_HIGH);
  radio.stopListening();

}

void loop() {
  message[0]=1;
  message[1]=1;
  message[2]=1;
  message[3]=1;
  message[4]=1;
  message[5]=1;
  message[6]=1;
  
  dummy = Serial.readString();

  for(int i = 0; i<dummy.length();i++){
    message[i] = dummy[i] - '0';
  }
  //Serial.println(" Send next Message0");
  radio.write(&message,sizeof(message));
  Serial.println(" Send next Message");
  delay(200);
}
