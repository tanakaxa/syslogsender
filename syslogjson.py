import socket
import json
import datetime

class SyslogData:
    # Create Syslog Message (RFC5424)
    def msgcreate(self, jsondata : json):
        SYSLOG_VERSION = 1

        try:
            facility = jsondata["facility"]
        except KeyError:
            # facility 16 : local0
            facility = 16

        try:
            severity = jsondata["severity"]
        except KeyError:
            # Severity 6 : Info
            severity = 6

        prival = facility * 8 + severity

        try:
            timestamp = jsondata["timestamp"]
        except KeyError:
            # Now JST Time
            utctime = datetime.datetime.now()
            # RFC3339 TimeStamp
            timestamp = utctime.isoformat() + "+09:00"

        try:
            hostname = jsondata["hostname"]
        except KeyError:
            hostname = "-"
        
        try:
            appname = jsondata["appname"]
        except KeyError:
            appname = "-"

        try:
            procid = jsondata["procid"]
        except KeyError:
            procid = "-"
        
        try:
            msgid = jsondata["msgid"]
        except KeyError:
            msgid = "-"     
        
        msg = jsondata["msg"]

        self.syslogmsg = "<%i>%i %s %s %s %s %s %s" % (
            prival,
            SYSLOG_VERSION,
            timestamp,
            hostname,
            appname,
            procid,
            msgid,
            msg
        )

    def __init__(self, jsondata : json):
        self.msgcreate(jsondata)

        self.server_ip = jsondata["logserver_ip"]
        
        try:
            self.server_port = jsondata["logserver_port"]
        except KeyError:
            # Default Syslog Port
            self.server_port = 514


# UDP syslog
class UdpSyslogData(SyslogData):
    def send(self):
        # Create UDP Socket Object
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send UDP Syslog
        client.sendto(self.syslogmsg.encode(), (self.server_ip, self.server_port))
        client.close()

        # Output Message
        print("Send To %s:%i MSG:%s" % (self.server_ip, self.server_port, self.syslogmsg))


# TCP syslog
class TcpSyslogData(SyslogData):
    def send(self):
        # Create TCP Socket Object
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Send TCP Syslog
        client.connect((self.server_ip, self.server_port))
        client.send(self.syslogmsg.encode())
        client.close()

        # Output Message
        print("Send To %s:%i(TCP) MSG:%s" % (self.server_ip, self.server_port, self.syslogmsg))