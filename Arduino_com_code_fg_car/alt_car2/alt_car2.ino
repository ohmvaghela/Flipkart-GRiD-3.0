char t;
const int r1=4,r2=5,l1=6,l2=9;
const int ena,enb;
 
void setup() {
Serial.begin(9600);
pinMode(r1,OUTPUT);   //right motors forward
pinMode(r2,OUTPUT);   //right motors reverse
pinMode(l1,OUTPUT);   //left motors forward
pinMode(l2,OUTPUT);   //left motors reverse
pinMode(ena,OUTPUT);
pinMode(enb,OUTPUT);
digitalWrite(ena,80);
digitalWrite(enb,80);
}
 
void loop() {
if(Serial.available()){
  t = Serial.read();
}
 
if(t == 'F'){            //move forward(all motors rotate in forward direction)
  digitalWrite(r1,HIGH);
  digitalWrite(r2,LOW);
  digitalWrite(l1,HIGH);
  digitalWrite(l2,LOW);
}
 
else if(t == 'B'){      //move reverse (all motors rotate in reverse direction)
  digitalWrite(r1,LOW);
  digitalWrite(r2,HIGH);
  digitalWrite(l1,LOW);
  digitalWrite(l2,HIGH);
}
 
else if(t == 'L'){      //turn right (left side motors rotate in forward direction, right side motors rotate in reverse direction for 100ms & stop)
  digitalWrite(r1,HIGH);
  digitalWrite(r2,LOW);
  digitalWrite(l1,LOW);
  digitalWrite(l2,HIGH);
  delay(100);
  t = 'S';
}
 
else if(t == 'R'){      //turn left (right side motors rotate in forward direction, left side motors rotate in reverse direction for 100ms & stop)
  digitalWrite(r1,LOW);
  digitalWrite(r2,HIGH);
  digitalWrite(l1,HIGH);
  digitalWrite(l2,LOW);
  delay(100);
  t = 'S';
}
 
else if(t == 'S'){      //STOP (all motors stop)
  digitalWrite(r1,LOW);
  digitalWrite(r2,LOW);
  digitalWrite(l1,LOW);
  digitalWrite(l2,LOW);
}
delay(100);
}
