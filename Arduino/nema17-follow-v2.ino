int xDir = 2;
int xPul = 3;

int yDir = 4;
int yPul = 5;

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
  while (!Serial.available())
    ;

  action = Serial.readString();

  if (action == "BR") {
    bottomRight();
  } else if (action == "TR") {
    topRight();
  } else if (action == "BL") {
    bottomLeft();
  } else if (action == "TL") {
    topLeft();
  } else {
    digitalWrite(xPul, LOW);
    digitalWrite(yPul, LOW);
  }


  // if (xCommand == "r") {
  //   goRight();
  // } else if (xCommand == "l") {
  //   goLeft();
  // } else {
  //   digitalWrite(xPul, LOW);
  // }

  // if (yCommand == "u") {
  //   goUp();
  // } else if (yCommand == "d") {
  //   goDown();
  // } else {
  //   digitalWrite(yPul, LOW);
  // }
}

void goUp() {
  for (int i = 0; i < 6400; i++) {
    digitalWrite(yDir, LOW);
    digitalWrite(yPul, HIGH);
    delayMicroseconds(100);
    digitalWrite(yPul, LOW);
    delayMicroseconds(100);
  }
}

void goDown() {
  for (int i = 0; i < 6400; i++) {
    digitalWrite(yDir, HIGH);
    digitalWrite(yPul, HIGH);
    delayMicroseconds(100);
    digitalWrite(yPul, LOW);
    delayMicroseconds(100);
  }
}

void goLeft() {
  for (int i = 0; i < 3200; i++) {
    digitalWrite(xDir, HIGH);
    digitalWrite(xPul, HIGH);
    delayMicroseconds(150);
    digitalWrite(xPul, LOW);
    delayMicroseconds(150);
  }
}

void goRight() {
  for (int i = 0; i < 3200; i++) {
    digitalWrite(xDir, LOW);
    digitalWrite(xPul, HIGH);
    delayMicroseconds(150);
    digitalWrite(xPul, LOW);
    delayMicroseconds(150);
  }
}

// -------------

void topLeft() {
  goUp();
  goLeft();
}

void topRight() {
  goUp();
  goRight();
}

void bottomLeft() {
  goDown();
  goLeft();
}

void bottomRight() {
  goDown();
  goRight();
}