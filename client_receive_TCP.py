#!/usr/bin/env python
################################################################
# Filename:    client_receive_rabbitmq.py
# Version:	   1
# Authoer:	   Lori
# Date:	       April 2018
# Description: Script for receiving KISS hex from TCP connection
################################################################

import math
import string
import time
import sys
import os
import datetime
import logging
import json
import serial
import binascii
import socket
import errno
import uuid

#from optparse import OptionParser
import argparse

FEND = 0xC0
FESC = 0xDB
TFEND = 0xDC
TFESC = 0xDD

def main():
    """ Main entry point to start the service. """

    startup_ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    #--------START Command Line argument parser------------------------------------------------------
    parser = argparse.ArgumentParser(description="Simple Serial TNC Connect and Print Program")

    net = parser.add_argument_group('Network Parameters')
    net.add_argument('--ip',
                       dest='ip',
                       type=str,
                       default='0.0.0.0',
                       help="IP Address",
                       action="store")
    net.add_argument('--port',
                       dest='port',
                       type=int,
                       default=9000,
                       help="IP Address",
                       action="store")

    args = parser.parse_args()
    #--------END Command Line argument parser------------------------------------------------------
    connected = False


    print 'Creating TCP Client Socket'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(1)
    try:
        sock.connect((args.ip, args.port))
        connected = True
    except:
        print "Failed to Connect to: [{:s}:{:d}]".format(args.ip, args.port)
        print "Is the server side running?...."
        sys.exit()

    packet_count = 0
    ax25_frames = []
    while connected:
        #try:
        data = sock.recv(1024)
        ts_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f UTC")
        if data:
            packet_count += 1
            print datetime.datetime.now(), "\t", binascii.unhexlify(data)

    
    sys.exit()


if __name__ == '__main__':
    main()

