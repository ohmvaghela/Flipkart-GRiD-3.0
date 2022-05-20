#include<SoftwareSerial.h>

#define IN1 4
#define IN2 5
#define IN3 6
#define IN4 9
#define EN1 3
#define EN2 10

SoftwareSerial mySerial(0, 1); // RX, TX

String data;
int btVal;

void setup() 
{  
  Serial.begin(9600);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(EN1, OUTPUT);
  pinMode(EN2, OUTPUT);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(EN1,80);
  analogWrite(EN2,80);
  mySerial.begin(9600);
}

void loop()
{
 while (mySerial.available())
 {  
  {  
      data = mySerial.readStringUntil('\n');
      Serial.print(data);             
  } 
    
    btVal = (data.toInt());
    Serial.print("BlueTooth Value \n");
    Serial.println(btVal);    



  if(btVal == 'F')
  {                                
        Serial.println("Forward \n");
        forward();
        break;
  }

  if(btVal == 'B')
  {                  
       Serial.println("Reverse \n");
        reverse();
        break;
  }

  if(btVal == 'L')
  {           
       Serial.println("Left \n");
        left();
        break;
  }
       
  if(btVal == 'R')
  {                       
        Serial.println("Right \n");
        right();
        break;
  }
        
  if(btVal == 'S')
  {                                              
        Serial.println("Stop \n");
        stoprobot();
        break;      

  }

 } 
 
                                                              
   if (mySerial.available() < 0)                              
    {
     Serial.println("No Bluetooth Data \n ");          
    }
  
}

void forward()
{
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void reverse()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void left()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(800);
  stoprobot();
}

void right()
{
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(800);
  stoprobot();
}

void stoprobot()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
