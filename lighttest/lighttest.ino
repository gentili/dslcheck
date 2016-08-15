void setup() {
  for (int i = 2; i <= 6; i++) { 
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  }
}

int pin = 2;
int dir = 1;
void loop() {
  digitalWrite(pin, LOW);
  pin += dir;
  if (pin > 6) {
    pin = 6;
    dir = -1;
  } else if (pin < 2) {
    pin = 2;
    dir = 1;
  }
  digitalWrite(pin, HIGH);
  delay(100);
}
