import json
import sys
from syslogjson import syslogjson

def main():
    # log message import
    logfile = open(sys.argv[1], 'r')
    jsonfile = json.load(logfile)

    for v in jsonfile.values():
        try:
            tcpflag = v["tcp"]
        except KeyError:
            tcpflag = False

        if tcpflag:
            item = syslogjson.TcpSyslogData(v)
        else:
            item = syslogjson.UdpSyslogData(v)
        
        item.send()

if __name__ == '__main__':
    main()
