#include <Servo.h>

int x;
Servo servoA;
void setup(){
  Serial.begin(9600);
  servoA.attach(10);
}

void loop(){
  if(Serial.available()>0){
    x=Serial.read();
    x=map(x,0,255,0,179);
    servoA.write(x);
  }
}
