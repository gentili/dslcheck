#include<Mailbox.h>

void setup() {
  Bridge.begin();
  Mailbox.begin();
  Console.begin();
  for (int i = 0; i < 7; i++) {
    pinMode(i+2,OUTPUT);
    digitalWrite(i+2, LOW);
  }
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  
}

String msg;
byte status[] = {0,0,0,0,0,0,0};
unsigned long lastmailcheck = 0;

void loop() {
  unsigned long curmillis = millis();
  unsigned long curslow = curmillis % 1000;
  unsigned long curfast = curmillis % 200;
  
  int msgsize = 0;
  if (curmillis - lastmailcheck > 100) {
    msgsize = Mailbox.messageAvailable();
    lastmailcheck = curmillis;
  }
  
  if (msgsize) {
    Mailbox.readMessage(msg);
    Console.println(msg);
    if (msg.length() != 8 || msg[0] != 'S') {
      Console.println("Bad Message");
      return;
    }
    for (int i = 0; i < 7; i++) {
      status[i] = byte(msg.charAt(i+1))-48;
    }
  }
  for (int i = 0; i < 7; i++) {
    if (status[i] == 0) {
      digitalWrite(i+2, LOW);
    } else
    if (status[i] == 1) {
      digitalWrite(i+2, HIGH);
    } else
    if (status[i] == 2) {
      if (curfast > 100)
        digitalWrite(i+2, HIGH);
      else
        digitalWrite(i+2, LOW);
    } else
    if (status[i] == 3) {
      if (curslow > 500)
        digitalWrite(i+2, HIGH);
      else
        digitalWrite(i+2, LOW);
    }
  }
}
