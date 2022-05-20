#include <SPI.h>
#include <RF24.h>

RF24 radio(7,8);
const byte address[6] = "00001";

const int frontButton = 6; //pressing button moves toy car forward
const int backButton = 5;  //pressing button moves toy car backward
const int leftButton = 4;  //pressing button moves toy car to left
const int rightButton = 3; //pressing button moves toy car to right
const int servo = 2; //pressing button moves servo motor
const int bot_id_1 = 0; //pressing button will command the specific robot
const int bot_id_2 = 1; //pressing button will command the specific robot
const int bot_id_3 = 9; //pressing button will command the specific robot
const int bot_id_4 = 10; //pressing button will command the specific robot
const int all_bot = A1; //pressing button will command all the robot

void setup() {
      // put your setup code here, to run once:
      pinMode(frontButton,INPUT_PULLUP);
      pinMode(backButton,INPUT_PULLUP);
      pinMode(leftButton,INPUT_PULLUP);
      pinMode(rightButton,INPUT_PULLUP);
      pinMode(servo,INPUT_PULLUP);
      pinMode(bot_id_1,INPUT_PULLUP);
      pinMode(bot_id_2,INPUT_PULLUP);
      pinMode(bot_id_3,INPUT_PULLUP);
      pinMode(bot_id_4,INPUT_PULLUP);
      pinMode(all_bot,INPUT_PULLUP);
      Serial.begin(9600);

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
      // put your main code here, to run repeatedly:
      int message[7];
      int bot1 = digitalRead(bot_id_1);
      int bot2 = digitalRead(bot_id_2);
      int bot3 = digitalRead(bot_id_3);
      int bot4 = digitalRead(bot_id_4);
      
      message[0] = digitalRead(frontButton);
      message[1] = digitalRead(backButton);
      message[2] = digitalRead(leftButton);
      message[3] = digitalRead(rightButton);
      message[4] = digitalRead(servo);
      message[5] = digitalRead(all_bot);
      
      int i;
      for (i = 0; i < 4; i = i + 1) {
            message[6]=0;
            if(bot1==0){
              message[6]=1;
            }
            if(bot2==0){
              message[6]=2;
            }
            if(bot3==0){
              message[6]=3;
            }
            if(bot4==0){
              message[6]=4;
            }
      }
      Serial.println("Transmitted");
      radio.write(&message,sizeof(message));
      delay(100);       //You can play with this number
}
