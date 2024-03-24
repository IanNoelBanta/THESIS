int dir = 2;
int pul = 3;

String x;

void setup() {
  pinMode(dir, OUTPUT);
  pinMode(pul, OUTPUT);

  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
  while (!Serial.available())
    ;

  x = Serial.readString();

  if (x == "r") {
    digitalWrite(dir, HIGH);
    generatePulses();
  }else if (x == "l") {
    digitalWrite(dir, LOW);
    generatePulses();
  } else {
    digitalWrite(pul, LOW);
  }
}

void generatePulses() {
  digitalWrite(pul, HIGH);  // Generate pulse
  digitalWrite(pul, LOW);
  delayMicroseconds(60);  // Delay between pulses
}