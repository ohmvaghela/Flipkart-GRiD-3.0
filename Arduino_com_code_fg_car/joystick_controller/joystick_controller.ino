#include <SPI.h>
#include <RF24.h>

RF24 radio(7,8);
const byte address[6] = "2Node";

int VRx = A0;
int VRy = A1;
int SW = 2;

int xPosition = 0;
int yPosition = 0;
int servo = 0;
int mapX = 0;
int mapY = 0;
uint16_t message;

void setup() {
  Serial.begin(9600); 
  
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(SW, INPUT_PULLUP); 

  radio.begin();
  Serial.println("checking if chip connected");
  bool check = radio.isChipConnected();
  Serial.print("check-");
  Serial.println(check);
  
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_HIGH);
  radio.stopListening();
  
}

void loop() {
  xPosition = analogRead(VRx);
  yPosition = analogRead(VRy);
  servo = digitalRead(SW);
  mapX = map(xPosition, 0, 1023, -512, 512);
  mapY = map(yPosition, 0, 1023, -512, 512);

  if(mapX<-400){
    message = 30256; //backward
  }
  else if(mapX>400){
    message = 26160; //forward
  }
  else if(mapY<-400){
    message = 32304; //left
  }
  else if(mapY>400){
    message = 28208; //right
  }
  else if(servo==0){
    message = 20016; //servo
  }
  else
  message = 17968; //stop

  bool report = radio.write(&message,sizeof(message));
  Serial.println(sizeof(message));
  if(!report){
    Serial.println("Transmission Failed");
  }
  else{
      Serial.println("Transmitted Successfull");
  }
  Serial.print(message);
  Serial.println();
}
