void setup() {
  for (int i = 2; i <= 9; i++) { 
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  }
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
}

int pin = 2;
int dir = 1;
void loop() {
  digitalWrite(pin, LOW);
  pin += dir;
  if (pin > 9) {
    pin = 9;
    dir = -1;
  } else if (pin < 2) {
    pin = 2;
    dir = 1;
  }
  digitalWrite(pin, HIGH);
  delay(100);
}
