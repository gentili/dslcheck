#include<Mailbox.h>

void setup() {
  pinMode(13, OUTPUT);
  for (int i = 0; i < 10; i++) {
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    delay(100);
  }
  digitalWrite(13, HIGH);
  Bridge.begin();
  Mailbox.begin();
  Console.begin();
  for (int i = 0; i < 8; i++) {
    pinMode(i+2,OUTPUT);
    digitalWrite(i+2, LOW);
  }
  Console.println("Waiting for boot");  
}

boolean booting = true;
String msg;
byte status[] = {0,0,0,0,0,0,0,0};
unsigned long lastmailcheck = 0;

void loop() {
  unsigned long curmillis = millis();
  unsigned long curslow = curmillis % 1000;
  unsigned long curfast = curmillis % 100;
  
  int msgsize = 0;
  if (curmillis - lastmailcheck > 100) {
    msgsize = Mailbox.messageAvailable();
    lastmailcheck = curmillis;
  }

  if (booting) {
      if (curslow > 500)
        digitalWrite(13, HIGH);
      else
        digitalWrite(13, LOW);
  }
  
  if (msgsize) {
    Mailbox.readMessage(msg);
    Console.println(msg);
    if (msg.length() != 9 || msg[0] != 'S') {
      Console.println("Bad Message");
      return;
    }
    if (booting) {
      booting = false;
      digitalWrite(13, HIGH);
      Console.println("Booted");
    }
    for (int i = 0; i < 8; i++) {
      status[i] = byte(msg.charAt(i+1))-48;
    }
  }
  for (int i = 0; i < 8; i++) {
    if (status[i] == 0) {
      digitalWrite(9-i, LOW);
    } else
    if (status[i] == 1) {
      digitalWrite(9-i, HIGH);
    } else
    if (status[i] == 2) {
      if (curfast > 50)
        digitalWrite(9-i, HIGH);
      else
        digitalWrite(9-i, LOW);
    } else
    if (status[i] == 3) {
      if (curslow > 500)
        digitalWrite(9-i, HIGH);
      else
        digitalWrite(9-i, LOW);
    }
  }
}
