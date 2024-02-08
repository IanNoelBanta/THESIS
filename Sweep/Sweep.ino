#include <Servo.h>

Servo myservo;

int pos = 0;

void setup() {
  Serial.begin(9600);
  myservo.attach(8);
}

void loop() {
  // continuous sweep movement
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }

  // Check if serial data is available
  if (Serial.available() > 0) {
    // Read the incoming byte
    char incomingByte = Serial.read();

    // If the incoming byte is 'r', reset the position to 0 degrees
    if (incomingByte == 'r') {
      myservo.write(0);
      myservo.write(180);  // Set servo position to 0 degrees
      delay(1000);
    }
  }
}
