#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from optparse import OptionParser
import sys

def _handleCmdLine(args):
    parser = OptionParser()
    parser.add_option("--host", dest="host",action="store", type="string", default="localhost",
            help="host")

    parser.add_option("--port", dest="port",action="store", type="int", default=0,
            help="port")

    parser.add_option("--timeout", dest="timeout",action="store", type="int", default=10,
            help="timeout")

    (options, args) = parser.parse_args(args)
    return (options,args)

def main():
    options,args=_handleCmdLine(sys.argv)
    host = options.host
    port = options.port
    if not host or port==0:
        print "Usage: --host <ip> --port <port>"
        sys.exit(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(options.timeout)
    s.connect((host, port))
    s.close()

if __name__ == '__main__':
    main()
