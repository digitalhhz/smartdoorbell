import datetime
import logging
import urllib2
 
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
    print 'Dash button pressed at ' + current_time
    urllib2.urlopen('https://maker.ifttt.com/trigger/poster_gillette/with/key/dxpJRFJ8zacPkgcM0wpjxWfYI6_ENMhjgaUmXH39ZxM')
 
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
 
mac_to_action = {'34:d2:70:d8:4d:37' : button_pressed_dash1}
mac_id_list = list(mac_to_action.keys())
 
print "Waiting for a button press..."
sniff(prn=udp_filter, store=0, filter="udp", lfilter=lambda d: d.src in mac_id_list)
 
if __name__ == "__main__":
  main()
