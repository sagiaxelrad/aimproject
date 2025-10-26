
#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial mySerial(A0, 11); // RX, TX
Servo movx;  
Servo movy; 

int x;
int y;
  
void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  mySerial.begin(9600);
  Serial.println("BEGIN");
  movx.attach(5);  
  movy.attach(6);  


}

void loop() { 
  if (mySerial.available()) {
    int len = mySerial.available();     
    byte buffer[len];                  
    mySerial.readBytes(buffer, len);
    Serial.write(buffer,len);
    Serial.println("gotcha");
    //float a, b;
    //if (sscanf(buffer, "(%f, %f)", &a, &b) == 2) 
    //{
     // x = (int)a;
     // y = (int)b;
   // }
    //Serial.println(a);
    //Serial.println(b);
  }
  Serial.println("gotcha");

}
