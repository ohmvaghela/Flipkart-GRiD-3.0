#include <SPI.h>
#include <RF24.h>
#include <Servo.h>

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "2Node";

Servo myservo;
int pos = 0;    // variable to store the servo position

//Motor1 is controlled by IN1 and IN2
//Motor2 is controlled by IN3 and IN4
const int ENA = 5;
const int ENB = 3;
const int IN1 = 4;
const int IN2 = 10;
const int IN3 = 6;
const int IN4 = 9;

void setup() {
      myservo.attach(2);
      pinMode(ENA,OUTPUT);
      pinMode(ENB,OUTPUT);
      pinMode(IN1,OUTPUT);
      pinMode(IN2,OUTPUT);
      pinMode(IN3,OUTPUT);
      pinMode(IN4,OUTPUT);
      Serial.begin(9600);
      
      radio.begin();
      Serial.println("checking if chip connected");
      bool check = radio.isChipConnected();
      Serial.print("check-");
      Serial.println(check);
      
      radio.openReadingPipe(0, address);
      radio.setPALevel(RF24_PA_MIN);
      radio.startListening();

      analogWrite(ENA, 100);
      analogWrite(ENB, 100);
}
void loop() {
      if (radio.available()) {
        int message;
        radio.read(&message, sizeof(message));      
        Serial.println(message);      
      }
}
