int xDir = 2;
int xPul = 3;
int yDir = 4;
int yPul = 5;
int speed = 500;  //CHANGE SPEED HERE
String action, xCommand, yCommand;
String prevAction = "";  // Variable to store the previous action

void setup() {
  pinMode(xDir, OUTPUT);
  pinMode(xPul, OUTPUT);
  pinMode(yDir, OUTPUT);
  pinMode(yPul, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
  while (!Serial.available())
    ;
  String currentAction= Serial.readString();

  if (currentAction == "r") {
    action = currentAction;
    Serial.print("Action: " + action);
    if (action == "r") {
      while (action == "r") {
        goRight();
        if (Serial.available() > 0) {
          currentAction = Serial.readString();
          if (currentAction != prevAction) {
            prevAction = currentAction;
            break;
          }
        }
      }
    }
  } else if (currentAction == "l") {
    action = currentAction;
    Serial.print("Action: " + action);
    if (action == "l") {
      while (action == "l") {
        goLeft();
        if (Serial.available() > 0) {
          currentAction = Serial.readString();
          if (currentAction != prevAction) {
            prevAction = currentAction;
            break;
          }
        }
      }
    }
  } else {
    digitalWrite(xPul, LOW);
  }
}

void goUp() {
  for (int i = 0; i < 200; i++) {
    digitalWrite(yDir, LOW);
    digitalWrite(yPul, HIGH);
    digitalWrite(yPul, LOW);
    delayMicroseconds(500);
  }
}

void goDown() {
  for (int i = 0; i < 200; i++) {
    digitalWrite(yDir, HIGH);
    digitalWrite(yPul, HIGH);
    digitalWrite(yPul, LOW);
    delayMicroseconds(500);
  }
}

void goLeft() {
  digitalWrite(xDir, HIGH);
  generatePulses();
}

void goRight() {
  digitalWrite(xDir, LOW);
  generatePulses();
}

void generatePulses() {
  digitalWrite(xPul, HIGH);
  digitalWrite(xPul, LOW);
  delayMicroseconds(speed);
}