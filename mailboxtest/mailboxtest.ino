#include <Mailbox.h>
void setup() {
  Bridge.begin();
  Mailbox.begin();
  Console.begin();
}

String msg;

void loop() {
  Mailbox.readMessage(msg);
  if (msg.length() > 0)
    Console.println(msg);
}
