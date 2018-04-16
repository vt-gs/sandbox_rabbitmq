#!/usr/bin/env python
################################################################
# Filename:    server_configure_rabbitmq.py
# Version:	   1
# Authoer:	   Lori 
# Date:	       April 2018
# Description: RabbitMQ Server Creation and Configuration
#
#    Includes code modified from https://stackoverflow.com/questions/11026959/writing-a-dict-to-txt-file-and-reading-it-back
#       [reading dictionary from file]
#    Includes code modified from https://www.rabbitmq.com/tutorials/tutorial-three-python.html
#       [interacting with RabbitMQ server]
#
################################################################

import pika                  # Communicate with RabbitMQ

# Setup configuration parameters
vhost =        "/"
exc =          "Kiss Exchange"
username =     "guest"
password =     "guest"

# Configure RabbitMQ connection
creds= pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', virtual_host = vhost, credentials = creds))
channel = connection.channel()
print "Connected to vhost '%s' on RMQ server at 'localhost' as user '%s'" % (vhost , username)

# Create a RabbitMQ direct exchange
channel.exchange_declare(exchange = exc, exchange_type='direct')

# Clear and setup specified routing keys and queues
#
# Used Routing Keys:
# kiss_hex_routing_key
# kiss_metadata_routing_key
#
# Used Queues:
# kiss_hex_queue_1
# kiss_hex_queue_2
# kiss_metadata_queue_1
# kiss_logs_queue_1

# Queue "Kiss Hex 1" is used for receiving kiss hex packets only
q = "kiss_hex_queue_1"
channel.queue_declare(queue = q)
channel.queue_purge(queue = q)
print "\r\nCreated queue: '%s'" %q
key = "kiss_hex_key"
channel.queue_unbind(exchange = exc, queue = q, routing_key = key)
channel.queue_bind(exchange = exc, queue = q, routing_key = key)
print "Bound to routing key: '%s'" % key
  
# Queue "Kiss Hex 2" is used for receiving kiss hex packets only
q = "kiss_hex_queue_2"
channel.queue_declare(queue = q)
channel.queue_purge(queue = q)
print "\r\nCreated queue: '%s'" %q
key = "kiss_hex_key"
channel.queue_unbind(exchange = exc, queue = q, routing_key = key)
channel.queue_bind(exchange = exc, queue = q, routing_key = key)
print "Bound to routing key: '%s'" % key

# Queue "Kiss Metadata" is used for receiving kiss metadata only
q = "kiss_metadata_queue_1"
channel.queue_declare(queue = q)
channel.queue_purge(queue = q)
print "\r\nCreated queue: '%s'" %q
key = "kiss_metadata_key"
channel.queue_unbind(exchange = exc, queue = q, routing_key = key)
channel.queue_bind(exchange = exc, queue = q, routing_key = key)
print "Bound to routing key: '%s'" % key

# Queue "Kiss Log" is used for receiving kiss hex packets and metadata
q = "kiss_logs_queue_1"
channel.queue_declare(queue = q)
channel.queue_purge(queue = q)
print "\r\nCreated queue: '%s'" %q
key = "kiss_hex_key"
channel.queue_unbind(exchange = exc, queue = q, routing_key = key)
channel.queue_bind(exchange = exc, queue = q, routing_key = key)
key = "kiss_metadata_key"
print "Bound to routing key: '%s'" % key
channel.queue_unbind(exchange = exc, queue = q, routing_key = key)
channel.queue_bind(exchange = exc, queue = q, routing_key = key)
print "Bound to routing key: '%s'" % key

