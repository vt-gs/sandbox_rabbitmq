#!/usr/bin/env python
################################################################
# Filename:    client_publish_kiss_rabbitmq.py
# Version:	   1
# Authoer:	   Lori
# Date:	       April 2018
# Description: RabbitMQ client that publishes test messages to RabbitMQ queues
################################################################

import pika
import argparse
import datetime
import time

# Parse the command line arguments
parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('required named arguments')

# Argument '-s' is required
requiredNamed.add_argument('-s', '--server', type=str, help='Server IP Address', required=True)
args = parser.parse_args()

# Setup configuration parameters
vhost =        "/"
exc =          "Kiss Exchange"
username =     "guest"
password =     "guest"

# Configure RabbitMQ connection
creds= pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=args.server, virtual_host = vhost, credentials = creds))
channel = connection.channel()
print("Connected to vhost '%s' on RMQ server at '%s' as user '%s'" % (vhost, args.server, username))

counter = 0
while(1):
    # Publish test message with hex routing key
    msg = "Hex message here " + str(counter)
    counter = counter + 1
    key = "kiss_hex_key"
    channel.basic_publish(exchange = exc, routing_key = key, body = msg)
    print datetime.datetime.now().time(), "\tPublished message with routing_key: '%s'" % key, " \tMessage: '%s'" %msg
    time.sleep(3)
    
    # Publish test message with metadata routing key
    msg = "Meta message here " + str(counter)
    counter = counter + 1
    key = "kiss_metadata_key"
    channel.basic_publish(exchange = exc, routing_key = key, body = msg)
    print datetime.datetime.now().time(), "\tPublished message with routing_key: '%s'" % key, " \tMessage: '%s'" %msg
    time.sleep(3)
	