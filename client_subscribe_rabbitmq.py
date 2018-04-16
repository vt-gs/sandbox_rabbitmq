################################################################
# Filename:    client_subscribe_kiss_rabbitmq.py
# Version:	   1
# Authoer:	   Lori
# Date:	       April 2018
# Description: RabbitMQ client that subscribes to various Kiss data queues
################################################################

import pika
import argparse
import datetime

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
print "Connected to vhost '%s' on RMQ server at '%s' as user '%s'" % (vhost, args.server, username)

# Ask terminal which queue to consume data from
queue_name = raw_input("Consume from Queue:")
print "Consuming messages from queue: '%s'" % queue_name

# Begin consuming from designated queue and print received message contents
def callback(ch, method, properties, body):
    print datetime.datetime.now().time(), "\tConsumed a message published with routing_key: '%s'" % method.routing_key, "\tMessage: %s" % body.decode()    
     
while (1):
    channel.queue_bind(exchange = exc, queue = queue_name)
    channel.basic_consume(callback, queue = queue_name , no_ack=True)
    channel.start_consuming()

	
