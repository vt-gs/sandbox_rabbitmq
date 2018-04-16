------Overview---------------------------------------------------------------------
This project performs the basic functions needed to: 
	(1) Receive a KISS packet in hexadecimal format over a TCP connection
	(2) Parse out the AX.25 frame and contents into a JSON object
	(3) Distribute the JSON object over RabbitMQ
	(4) Receive the JSON object from a RabbitMQ queue and parse out the original KISS packet in hexadecimal format
	(5) Forward the KISS hex packet to a TCP connection 

See the included block diagrams for a visual overview of how the scripts relate.


------Setting Up the RabbitMQ Server------------------------------------------------
After installing the RabbitMQ package, enable the management plugin to gain access to the browser management console:
	
	sudo rabbitmq-plugins enable rabbitmq_management
	
Start the RabbitMQ Server in the background:
	
	sudo rabbitmq-server service restart

Run the following python configuration file to setup the exchange and queues used:

	python server_configure_rabbitmq.py
	
Navigate to http://127.0.0.1:15672/#/ and use username: guest and password: guest to keep an eye on the Rabbit MQ side of things	
	
	
------Simple KISS Playback/Receive Scripts-----------------------------------------	
To demonstrate simple sending and receiving of KISS hex packets over TCP, the following scripts can be executed:
Send KISS hex packets:	

	python kiss_net_playback.py --kiss_file [KISS_FILE]
		
Receive KISS hex packets and parse contents:

	python kiss_net_rx.py


------Simple Send/Receive Using RabbitMQ------------------------------------------------
To demonstrate simple sending and receiving of messages using RabbitMQ, the following scripts can be executed.  A separate instance of the receive script must be executed for each queue that you want to receive from.  The list of queues and routing keys can be found below.  
Send test messages:	

	python client_publish_test_rabbitmq.py
		
Receive test messages:

	client_subscribe_rabbitmq.py

[As configured in the RabbitMQ server scritpt] 
QUEUE; 			ASSOCIATED ROUTING KEY(S):
kiss_hex_queue_1; 	kiss_hex_routing_key	
kiss_hex_queue_2; 	kiss_hex_routing_key
kiss_metadata_queue_1; 	kiss_metadata_routing_key
kiss_logs_queue_1; 	kiss_hex_routing_key, kiss_metadata_routing_key


------Full Functionality------------------------------------------------
To demonstrate full functionality of the system, the following scripts can be executed:
Send KISS hex packets over TCP:

	python kiss_net_playback.py --kiss_file [KISS_FILE]
		
Receive KISS hex packets and parse contents into JSON objects that are distributed over RabbitMQ:

	python client_rx_kiss_to_rabbitmq.py

Receive KISS JSON objects over RabbitMQ and forward the KISS hex packets over TCP connection:

	python client_forward_rabbitmq.py
	
Receive KISS hex packets over TCP connection:

	python client_receive_TCP.py











