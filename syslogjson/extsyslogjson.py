from scapy.all import*
from random import randrange
from syslogjson import syslogjson
import json
import datetime

# UDP Custum SrcIP syslog
class ExtUdpSyslogData(syslogjson.SyslogData):
    def __init__(self, jsondata : json):
        try:
            rfc5424flag = jsondata["rfc5424"]
        except KeyError:
            rfc5424flag = False

        if rfc5424flag:
            self.msgcreate5424(jsondata)
        else:
            self.msgcreate3164(jsondata)

        self.server_ip = jsondata["logserver_ip"]
        
        try:
            self.server_port = jsondata["logserver_port"]
        except KeyError:
            # Default Syslog Port
            self.server_port = 514
        
        self.srcip = jsondata["custom_srcip"]


    def send(self):
        # Send Message
        send(IP(src=self.srcip, dst=self.server_ip)/UDP(sport=randrange(1024, 65536), dport=self.server_port)/self.syslogmsg, verbose=0)

        # Output Message
        print("Send From %s To %s:%i MSG:%s" % (self.srcip, self.server_ip, self.server_port, self.syslogmsg))
