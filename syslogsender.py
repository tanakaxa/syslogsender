import socket
import json
import datetime
import sys

SYSLOG_VERSION = 1

# Create Now JST TimeStamp
def timecreate():
    utctime = datetime.datetime.now()

    # RFC3339 TimeStamp
    timestamp = utctime.isoformat() + "+09:00"

    return timestamp

# Create Syslog Message (RFC5424)
def msgcreate(jsondata : json):   
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
        timestamp = timecreate()

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

    log = "<%i>%i %s %s %s %s %s %s" % (
        prival,
        SYSLOG_VERSION,
        timestamp,
        hostname,
        appname,
        procid,
        msgid,
        msg
    )

    return log

# log message import
logfile = open(sys.argv[1], 'r')
jsonfile = json.load(logfile)

for v in jsonfile.values():
    # Create Syslog Mesage
    syslog_message = msgcreate(v)


    server_ip = v["logserver_ip"]
    try:
        server_port = v["logserver_port"]
    except KeyError:
        # Default Syslog Port
        server_port = 514


    # Protocol
    try:
        tcpflag = v["tcp"]
    except KeyError:
        tcpflag = False
    
    # Send Syslog
    if tcpflag:
        # Create TCP Socket Object
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Send TCP Syslog
        client.connect((server_ip, server_port))
        client.send(syslog_message.encode())
        print("Send To %s:%i(TCP) MSG:%s" % (server_ip, server_port, syslog_message))
    else:
        # Create UDP Socket Object
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Send UDP Syslog
        client.sendto(syslog_message.encode(), (server_ip, server_port))
        print("Send To %s:%i MSG:%s" % (server_ip, server_port, syslog_message))

    client.close()