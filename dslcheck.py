#!/usr/bin/python -u

import sys
sys.path.insert(0,"/usr/lib/python2.7/bridge/")
from bridgeclient import BridgeClient
from subprocess import CalledProcessError, check_output
import re
import time
import ConfigParser
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.ConfigParser()
filelist = config.read(scriptdir + "/dslcheck.cfg")
if len(filelist) == 0:
    print "ERR: missing dslcheck.cfg configuration"
    sys.exit(1)

wifidevice = config.get("dslcheck","wifidevice")
apaddr = config.get("dslcheck","apaddr")
gatewayprivateaddr = config.get("dslcheck","gatewayprivateaddr")
gatewaypublicaddr = config.get("dslcheck","gatewaypublicaddr")
gatewaypeeraddr = config.get("dslcheck","gatewaypeeraddr")
remoteaddr = config.get("dslcheck","remoteaddr")
        
addrregex = r"addr:(\d+\.\d+\.\d+\.\d+)"

client = BridgeClient()

#print "Sending text to mailbox"
#client.mailbox("Hi there")

class DSLCheckException(Exception):
       def __init__(self, arg):
            self.step = arg

       def getstep(self):
            return self.step

def try_command(step, errname, commandline):
    try:
        return check_output(commandline)
    except CalledProcessError:
        print errname
        raise DSLCheckException(step)

while True:
    try:
        curstep = 0
        print "Check if wifi is running"
        retval = try_command(curstep,"ERR: wifi interface missing", ["ifconfig", wifidevice])
        curstep += 1

        print "Check if ip address is assigned"
        match = re.search(addrregex,retval)
        if not match:
            print "ERR: no ip address assigned to wifi"
            raise DSLCheckException(curstep)
        localip = match.group(1)
        curstep += 1

        print "Check if we can ping the access point"
        retval = try_command(curstep,"ERR: can't ping access point", ["ping","-q","-c","1","-W","4",apaddr])
        curstep += 1

        print "Check if we can ping the border gateway internal address"
        retval = try_command(curstep,"ERR: can't ping border gateway private address", ["ping","-q","-c","1","-W","4",gatewayprivateaddr])
        curstep += 1

        print "Check if we can ping the border gateway public address"
        retval = try_command(curstep,"ERR: can't ping border gateway public address", ["ping","-q","-c","1","-W","4",gatewaypublicaddr])
        curstep += 1

        print "Check if we can ping the ptp peer"
        retval = try_command(curstep,"ERR: can't ping border gateway peer address", ["ping","-q","-c","1","-W","4",gatewaypeeraddr])
        curstep += 1

        print "Check if we can ping remote address"
        retval = try_command(curstep,"ERR: can't ping remote address", ["ping","-q","-c","1","-W","4",remoteaddr])
    except DSLCheckException as e:
        print "Failed check {}".format(e.getstep())

    time.sleep(1)
