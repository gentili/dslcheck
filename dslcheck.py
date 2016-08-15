#!/usr/bin/python

import sys
sys.path.insert(0,"/usr/lib/python2.7/bridge/")
from bridgeclient import BridgeClient

client = BridgeClient()

print "Sending text to mailbox"
client.mailbox("Hi there")
print "Receiving from mailbox"
print client.getall()
