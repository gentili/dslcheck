#!/usr/bin/python -u

import sys
sys.path.insert(0,"/usr/lib/python2.7/bridge/")
from bridgeclient import BridgeClient
from subprocess import CalledProcessError, check_output
import re
import time
import ConfigParser
import os
import datetime

scriptdir = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.ConfigParser()
filelist = config.read(scriptdir + "/dslcheck.cfg")
if len(filelist) == 0:
    print "ERR: missing dslcheck.cfg configuration"
    sys.exit(1)

wifidevice = config.get("dslcheck","wifidevice")
wificarrierfile = config.get("dslcheck","wificarrierfile")
apaddr = config.get("dslcheck","apaddr")
gatewayprivateaddr = config.get("dslcheck","gatewayprivateaddr")
gatewaypublicaddr = config.get("dslcheck","gatewaypublicaddr")
gatewaypeeraddr = config.get("dslcheck","gatewaypeeraddr")
remoteaddr = config.get("dslcheck","remoteaddr")
        
addrregex = r"addr:(\d+\.\d+\.\d+\.\d+)"

client = BridgeClient()

leds = [0,0,0,0,0,0,0,0]

# 0 = OFF
# 1 = ON
# 2 = HALFDUTY
# 3 = FLASH


class DSLCheckException(Exception):
       def __init__(self, arg):
            self.step = arg

       def getstep(self):
            return self.step

def t_print(msg):
    print "{:%Y-%b-%d %H:%M:%S} - ".format(datetime.datetime.now())+msg

def try_command(step, errname, commandline):
    try:
        return check_output(commandline)
    except CalledProcessError:
        t_print (errname)
        raise DSLCheckException(step)

def led_set(step,value):
    leds[step] = value

def led_clear_set(step,value):
    for i in range(step,len(leds)):
        leds[i] = 0
    leds[step] = value

def led_tx():
    msg = 'S';
    for i in leds:
        msg += str(i)
    client.mailbox(msg)


while True:
    try:
        curstep = 0
        t_print("Check if wifi is running")
        led_set(curstep,2)
        led_tx()
        wificonf = try_command(curstep,"ERR: wifi interface missing", ["ifconfig", wifidevice])
        time.sleep(1)
        led_set(curstep,1)
        curstep += 1

        t_print("Check if wifi is connected")
        led_set(curstep,2)
        led_tx()
        carrier = try_command(curstep,"ERR: wifi carrier status unknown", ["cat", wificarrierfile])
        if (carrier[:1] != "1"):
            t_print("ERR: wifi carrier not present" + carrier)
            raise DSLCheckException(curstep)
        time.sleep(1)
        led_set(curstep,1)
        curstep += 1

        t_print("Check if ip address is assigned")
        led_set(curstep,2)
        led_tx()
        match = re.search(addrregex,wificonf)
        if not match:
            t_print("ERR: no ip address assigned to wifi")
            raise DSLCheckException(curstep)
        time.sleep(1)
        led_set(curstep,1)
        curstep += 1

        t_print("Check if we can ping the access point")
        led_set(curstep,2)
        led_tx()
        try_command(curstep,"ERR: can't ping access point", ["ping","-q","-c","1","-W","4",apaddr])
        time.sleep(1)
        led_set(curstep,1)
        curstep += 1

        t_print("Check if we can ping the border gateway internal address")
        led_set(curstep,2)
        led_tx()
        try_command(curstep,"ERR: can't ping border gateway private address", ["ping","-q","-c","1","-W","4",gatewayprivateaddr])
        time.sleep(1)
        led_set(curstep,1)
        curstep += 1

        t_print("Check if we can ping the border gateway public address")
        led_set(curstep,2)
        led_tx()
        try_command(curstep,"ERR: can't ping border gateway public address", ["ping","-q","-c","1","-W","4",gatewaypublicaddr])
        time.sleep(1)
        led_set(curstep,1)
        curstep += 1

        t_print("Check if we can ping the ptp peer")
        led_set(curstep,2)
        led_tx()
        try_command(curstep,"ERR: can't ping border gateway peer address", ["ping","-q","-c","1","-W","4",gatewaypeeraddr])
        time.sleep(1)
        led_set(curstep,1)
        curstep += 1

        t_print("Check if we can ping remote address")
        led_set(curstep,2)
        led_tx()
        try_command(curstep,"ERR: can't ping remote address", ["ping","-q","-c","1","-W","4",remoteaddr])
        time.sleep(1)
        led_set(curstep,1)
    except DSLCheckException as e:
        t_print("Failed check {}".format(e.getstep()))
        led_clear_set(e.getstep(),3)

    led_tx()
    time.sleep(5)
