#include <ezButton.h>
#include <Servo.h>

Servo myservo;

// ezButton limitSwitchUP(8);
ezButton limitSwitchDOWN(9); //9
ezButton limitSwitchLEFT(10);
ezButton limitSwitchRIGHT(11);
ezButton limitSwitchAMPALAYA(12);
// ezButton limitSwitchFORWARD(11);
ezButton limitSwitchBACK(13);

int xDir = 2;
int xPul = 3;
int yDir = 4;
int yPul = 5;
int zDir = 6;
int zPul = 7;

int xSpeed = 500;
int ySpeed = 700;
int zSpeed = 60;


String action, xCommand, yCommand;
String prevAction = "";

void setup() {
  pinMode(xDir, OUTPUT);
  pinMode(xPul, OUTPUT);
  pinMode(yDir, OUTPUT);
  pinMode(yPul, OUTPUT);
  pinMode(zDir, OUTPUT);
  pinMode(zPul, OUTPUT);
  myservo.attach(8);
  myservo.write(60); //35

  Serial.begin(9600);
  Serial.setTimeout(1);

  // limitSwitchUP.setDebounceTime(50);
  limitSwitchDOWN.setDebounceTime(50);
  limitSwitchLEFT.setDebounceTime(50);
  limitSwitchRIGHT.setDebounceTime(50);
  limitSwitchAMPALAYA.setDebounceTime(50);
  limitSwitchBACK.setDebounceTime(50);
}

void loop() {
  while (!Serial.available())
    ;
  String currentAction = Serial.readString();

  if (currentAction == "r") {
    action = currentAction;
    if (action == "r") {
      while (action == "r" && !limitSwitchRIGHT.isPressed()) {
        limitSwitchRIGHT.loop();
        goRight();
        if (Serial.available() > 0) {
          currentAction = Serial.readString();
          if (currentAction != prevAction) {
            prevAction = currentAction;
            break;
          }
        }
      }
      limitSwitchRIGHT.loop();
    }
  } else if (currentAction == "l") {
    action = currentAction;
    if (action == "l") {
      while (action == "l" && !limitSwitchLEFT.isPressed()) {
        limitSwitchLEFT.loop();
        goLeft();
        if (Serial.available() > 0) {
          currentAction = Serial.readString();
          if (currentAction != prevAction) {
            prevAction = currentAction;
            break;
          }
        }
      }
      limitSwitchLEFT.loop();
    }
  } else if (currentAction == "u") {
    action = currentAction;
    if (action == "u") {
      while (action == "u") {
        // limitSwitchUP.loop();
        goUp();
        if (Serial.available() > 0) {
          currentAction = Serial.readString();
          if (currentAction != prevAction) {
            prevAction = currentAction;
            break;
          }
        }
      }
      // limitSwitchUP.loop();
    }
  } else if (currentAction == "d") {
    action = currentAction;
    if (action == "d") {
      while (action == "d" && !limitSwitchDOWN.isPressed()) {
        limitSwitchDOWN.loop();
        goDown();
        if (Serial.available() > 0) {
          currentAction = Serial.readString();
          if (currentAction != prevAction) {
            prevAction = currentAction;
            break;
          }
        }
      }
      limitSwitchDOWN.loop();
    }
  } else if (currentAction == "f") {
    action = currentAction;
    if (action == "f") {
      while (action == "f" && !limitSwitchAMPALAYA.isPressed()) {
        limitSwitchAMPALAYA.loop();
        goForward();
        if (Serial.available() > 0) {
          currentAction = Serial.readString();
          if (currentAction != prevAction) {
            prevAction = currentAction;
            break;
          }
        }
      }
      limitSwitchAMPALAYA.loop();
    }
  } else if (currentAction == "b") {
    action = currentAction;
    if (action == "b") {
      while (action == "b" && !limitSwitchBACK.isPressed()) {
        limitSwitchBACK.loop();
        goBack();
        if (Serial.available() > 0) {
          currentAction = Serial.readString();
          if (currentAction != prevAction) {
            prevAction = currentAction;
            break;
          }
        }
      }
      limitSwitchBACK.loop();
    }
  } else {
    if (currentAction == "x") {
      digitalWrite(xPul, LOW);
    } else if (currentAction == "y") {
      digitalWrite(yPul, LOW);
    } else if (currentAction == "z") {
      goZ();
    }
  }
  // goDown();
  
}

void goLeft() {
  digitalWrite(xDir, HIGH);
  generateXPulses();
}

void goRight() {
  digitalWrite(xDir, LOW);
  generateXPulses();
}

void goUp() {
  digitalWrite(yDir, LOW);
  generateYPulses();
}

void goDown() {
  digitalWrite(yDir, HIGH);
  generateYPulses();
}

void goForward() {
  digitalWrite(zDir, LOW);
  generateZPulses();
}

void goBack() {
  digitalWrite(zDir, HIGH);
  generateZPulses();
}

void generateXPulses() {
  digitalWrite(xPul, HIGH);
  digitalWrite(xPul, LOW);
  delayMicroseconds(xSpeed);
}

void generateYPulses() {
  digitalWrite(yPul, HIGH);
  digitalWrite(yPul, LOW);
  delayMicroseconds(ySpeed);
}

void generateZPulses() {
  digitalWrite(zPul, HIGH);
  digitalWrite(zPul, LOW);
  delayMicroseconds(zSpeed);
}

void goZ() {
  // open();
  delay(2000);
  while (!limitSwitchAMPALAYA.isPressed()) {
    limitSwitchAMPALAYA.loop();
    goForward();
  }
  limitSwitchAMPALAYA.loop();
  digitalWrite(zPul, LOW);
  delay(2000);
  close();
  delay(2000);
  goZBack();
  delay(2000);
  goBasket();
  delay(2000);
  goZDown();
  delay(2000);
  open();
}

void open() {
  myservo.write(80);
}

void close() {
  myservo.write(180);
}

void goZBack() {
  while (!limitSwitchBACK.isPressed()) {
    limitSwitchBACK.loop();
    goBack();
  }
  limitSwitchBACK.loop();
  digitalWrite(zPul, LOW);
}

void goZDown() {
  while (!limitSwitchDOWN.isPressed()) {
    limitSwitchDOWN.loop();
    goDown();
  }
  limitSwitchDOWN.loop();
  digitalWrite(yPul, LOW);
}

void goBasket() {
  for (int i = 0; i < 32000; i++) {
    digitalWrite(zDir, LOW);
    digitalWrite(zPul, HIGH);
    digitalWrite(zPul, LOW);
    delayMicroseconds(zSpeed);
  }
}