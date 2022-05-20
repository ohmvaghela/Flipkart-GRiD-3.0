const int r1=4,r2=5,l1=6,l2=9;
const int ena=3,enb=10;
 
void setup() {
Serial.begin(9600);
pinMode(r1,OUTPUT);   //right motors forward
pinMode(r2,OUTPUT);   //right motors reverse
pinMode(l1,OUTPUT);   //left motors forward
pinMode(l2,OUTPUT);   //left motors reverse
pinMode(ena,OUTPUT);
pinMode(enb,OUTPUT);
digitalWrite(ena,10);
digitalWrite(enb,10);
digitalWrite(r1,LOW);
digitalWrite(r2,HIGH);
digitalWrite(l1,LOW);
analogWrite(l2,HIGH);
}
 
void loop(){
  
}
