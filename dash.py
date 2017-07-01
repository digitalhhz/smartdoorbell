#!/usr/bin/python2
# -*- coding: utf-8 -*-
# import os


import datetime
import logging
import requests  # Use requests to trigger the ITTT webhook

from send_mail import send_mail  # This function sends mails directly

 
# Constants
timespan_threshhold = 3
 
# Globals
lastpress = datetime.datetime(1970,1,1)
 
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

 
def button_pressed_dash1():
  global lastpress
  thistime = datetime.datetime.now()
  timespan = thistime - lastpress
  if timespan.total_seconds() > timespan_threshhold:
    current_time = datetime.datetime.strftime(thistime, '%Y-%m-%d %H:%M:%S')
    print 'Dash button nobo pressed at ' + current_time
    #requests.get("https://maker.ifttt.com/trigger/button_nobo/with/key/brsvXJ5YsJRbj8EMr1OnRN")
    send_mail("iotdashbutton77@gmail.com", subject="Bitte die Tuere oeffnen",text="Hallo,\n\ndie Klingel der unteren Tuere wurde gerade gedrueckt.\n\nViele Grüße,\n  dein Raspi") 
  lastpress = thistime

def button_pressed_dash2():
  global lastpress
  thistime = datetime.datetime.now()
  timespan = thistime - lastpress
  if timespan.total_seconds() > timespan_threshhold:
    current_time = datetime.datetime.strftime(thistime, '%Y-%m-%d %H:%M:%S')
    print 'Dash button Nerf pressed at ' + current_time
    requests.get("https://maker.ifttt.com/trigger/button_nerf/with/key/brsvXJ5YsJRbj8EMr1OnRN")
    send_mail("iotdashbutton77@gmail.com", subject="Bitte die Tuere oeffnen",text="Hallo,\n\ndie Klingel der oberen Tuere wurde gerade gedrueckt.\n\nViele Grüße,\n  dein Raspi") 
  lastpress = thistime
 
def udp_filter(pkt):
  if pkt.haslayer(DHCP):
    options = pkt[DHCP].options
    for option in options:
      if isinstance(option, tuple):
        if 'requested_addr' in option:
          # we've found the IP address, which means its the second and final UDP request, so we can trigger our action
          mac_to_action[pkt.src]()
          break
  else: pass
 
mac_to_action = {'ac:63:be:63:2c:14' : button_pressed_dash1, '34:d2:70:b6:31:01' : button_pressed_dash2}
mac_id_list = list(mac_to_action.keys())
 
print "Waiting for a button press..."
sniff(prn=udp_filter, store=0, filter="udp", lfilter=lambda d: d.src in mac_id_list)
 
if __name__ == "__main__":
  main()
