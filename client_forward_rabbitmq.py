#!/usr/bin/env python
################################################################
# Filename:    client_forward_rabbitmq.py
# Version:	   1
# Authoer:	   Lori
# Date:	       April 2018
# Description: Script for receiving KISS hex from RabbitMQ and forwards them to TCP connection
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

import pika
import argparse
import datetime

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


    #--------START Connect to RabbitMQ Server------------------------------------------------------
    # Setup configuration parameters
    vhost =        "/"
    exc =          "Kiss Exchange"
    username =     "guest"
    password =     "guest"
    server =       "127.0.0.1"

    # Configure RabbitMQ connection
    creds= pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=server, virtual_host = vhost, credentials = creds))
    channel = connection.channel()
    print("Connected to vhost '%s' on RMQ server at '%s' as user '%s'" % (vhost, server, username))

    #--------END Connect to RabbitMQ Server------------------------------------------------------
        

    #--Wait for connection from Client
    cont = 1
    while 1:
        print 'Creating TCP Server'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((args.ip, args.port))
        sock.listen(1)
        print "KISS packet forwarding begins on client connection"
        print "Server listening on: [{:s}:{:d}]".format(args.ip, args.port)
        conn, client = sock.accept()
        print "Connection from client: [{:s}:{:d}]".format(client[0], client[1])
        print "Beginning forwarding..."
        
        # Define RabbitMQ queue to consume data from
        queue_name = "kiss_hex_queue_1"
        print "Consuming messages from queue: '%s'" % queue_name

        while cont:
            channel.queue_bind(exchange = exc, queue = queue_name)
            method_frame, header_frame, body = channel.basic_get(queue = queue_name, no_ack = True)        
           
            if method_frame != None and method_frame.NAME != 'Basic.GetEmpty':
                try:
                    parsed_json = json.loads(body.decode())
                    message = parsed_json['kiss_hex']
                    print "Sending: ",  message
                    msg = binascii.hexlify(message)
                    try:
                        conn.sendall(bytearray(msg))
                    except socket.error, v:
                        errorcode=v[0]
                        if errorcode==errno.EPIPE:  #Client disconnected
                            print 'Client Disconnected'
                            cont = 0
                        break
                except:
                    print "Could not parse JSON"
                
        conn.close()
        print 'Finished Forwarding'
        cont = 1
    sys.exit()


if __name__ == '__main__':
    main()

