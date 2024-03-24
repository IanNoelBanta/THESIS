int xDir = 2;
int xPul = 3;

int yDir = 4;
int yPul = 5;

int upButton = 8;
int downButton = 9;
int leftButton = 10;
int rightButton = 11;

String action, xCommand, yCommand;

void setup() {
  pinMode(xDir, OUTPUT);
  pinMode(xPul, OUTPUT);

  pinMode(yDir, OUTPUT);
  pinMode(yPul, OUTPUT);

  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
  while (!Serial.available());
  action = Serial.readString();

// ---------- BUTTON ---------- 

  if (digitalRead(upButton)) {
    action = "UP";
  } else if (digitalRead(downButton)) {
    action = "DOWN";
  } else if (digitalRead(leftButton)) {
    action = "LEFT";
  } else if (digitalRead(rightButton)) {
    action = "RIGHT";

  } else if (digitalRead(upButton) && digitalRead(rightButton)) {
    action = "UR";
  } else if (digitalRead(upButton) && digitalRead(leftButton)) {
    action = "UL";
  } else if (digitalRead(downButton) && digitalRead(rightButton)) {
    action = "DR";
  } else if (digitalRead(downButton) && digitalRead(leftButton)) {
    action = "DL";
  } else {
    action = "null";
  }

// ---------- UP, DOWN, LEFT, AND RIGHT ---------- 
  if (action == "UP") { 
    goUp();
  } else if (action == "DOWN") {
    goDown();
  } else if (action == "LEFT") {
    goLeft();
  } else if (action == "RIGHT") {
    goRight();

// ---------- UP-RIGHT, UP-LEFT, DOWN-RIGHT, AND DOWN-LEFT ---------- 

  } else if (action == "UR") {
    goUp();
    goRight();
  } else if (action == "UL") {
    goUp();
    goLeft();
  } else if (action == "DR") {
    goDown();
    goRight();
  } else if (action == "DL") {
    goDown();
    goLeft();

// ---------- STOP ON ORIGIN ---------- 

  } else {
    digitalWrite(xPul, LOW);
    digitalWrite(yPul, LOW);
  }

}

// ----------- PULSE GENERATORS ----------- //

void generateXPulses() {
  digitalWrite(xPul, HIGH); // Generate pulse
  digitalWrite(xPul, LOW);
  delayMicroseconds(60);    // Delay between pulses
}

void generateYPulses() {
  digitalWrite(xPul, HIGH); // Generate pulse
  digitalWrite(xPul, LOW);
  delayMicroseconds(60);    // Delay between pulses
}

void goUp() {
    digitalWrite(yDir, LOW);
    generateYPulses();
}

void goDown() {
    digitalWrite(yDir, HIGH);
    generateYPulses();
}

void goLeft() {
    digitalWrite(xDir, HIGH);
    generateXPulses();
}

void goRight() {
    digitalWrite(xDir, LOW);
    generateXPulses();
}