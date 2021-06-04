import processing.serial.*;
Serial myport;

PFont font;

int x;
int offset=10;

void setup(){
  size(256,150);
  myport=new Serial(this,Serial.list()[2],9600);
}
 

void draw(){
  background(204);
  line(x,0,x,150);
  if(mouseX>x){x+=1; offset=10;}
  
  if(mouseX<x){x-=1; offset=-10;}
  
  fill(0);
  text(x,x,145);
  
  text(mouseX,mouseX,mouseY-15);
  line(mouseX,mouseY,mouseX+offset*3,mouseY);
  line(mouseX,mouseY,mouseX+offset,mouseY-10);
  line(mouseX,mouseY,mouseX+offset,mouseY+10);
  
  myport.write(mouseX);
}