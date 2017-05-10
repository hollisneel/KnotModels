#!/usr/bin/python
import argparse
import tempfile
import os
import subprocess
import re
import sys
import atexit
import time
import shutil
import boto.sqs
from boto.sqs.message import Message

'''
    loadqueue.py

    written by: Nicholas Neel

    Purpose : To interface into amazon web services to utilize their
    cloud computing capabilities.

    Usage example: 
    
    $ python loadqueue.py 5 100 2000

    created messages to upload...
    uploaded 1 messages out of 1
    Finished Creating Queue

    $

'''


# Place Amazon Web Services access key, secret access key, and region here
aki = open('/home/hollis/Documents/awsWebID.txt')
ask = open('/home/hollis/Documents/awsSecKey.txt')

access_key_id     = aki.read().replace('\n','').replace(' ','')
secret_access_key = ask.read().replace('\n','').replace(' ','')
region            = "us-east-1"
queue_name        = "StarData"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='load job description messages into SQS queue for classification')
	parser.add_argument(
	                    'integer',
						nargs=3,
						 type=str, 
	                     help='1) number of chords, 2) number of desired data points, 3) approx number of data pts per hour.')

    ### Phase One : Create messages ###

    # Set up command line input interface
	args = parser.parse_args()

    # var = # of points on star
	var = int(args.integer[0]) 

    # num = # of desired data points
	num = int(args.integer[1]) 

    # lim = computation speed per hour
	lim = int(args.integer[2]) 

    # Temporary variable for modifying number of remaining data points
	temp = int(num)

    # Paired with worker for format [#star, ]
	pts_list = [int(lim)]

    # Creates a bite sized workload for each worker node (ex: If each computer can 
    # handle 5 jobs and we have 23 desired jobs we obtain [5,5,5,5,3] so we need a total of five job messages created)
	while temp > 0:
		temp = temp - lim
		if temp > 0:
			pts_list.append(int(lim))
		if temp < 0:
			pts_list.remove(lim)
			pts_list.append(lim + temp)

    # Create actual message to be parsed by worker.
	messages = []
	for a in range(len(pts_list)):
		messages.append(str(var) + "," + str(pts_list[a]))


    # Stupid check that we actually obtain number of desired points.
	summ = 0
	for a in pts_list:
		summ += a
	if summ != lim:
		print "Bug in code: incorrect numbner of data pts"
		print summ, lim
		sys.exit(1)

	print "Created Messages to upload..."


    # Now we have created our queue messages!



	### Phase Two: Log into AWS and upload messages ###


    # Takes credentials from the header 
	conn = conn = boto.sqs.connect_to_region(region,aws_access_key_id=acess_key_id,aws_secret_access_key=secret_access_key)
	queue = conn.get_all_queues(prefix=queue_name)[0]
	count = 0
	for a in messages:
		count += 1
        
        # Create new message object
		new_message = queue.new_message()
        # Put message info in the message object
		new_message.set_body(a)
        # Write message to queue
		queue.write(new_message)
        
        # Progress checking
		if count % 100 == 0:
			print "Uploaded " + str(count) + " messages out of " + str(len(messages)) + " ..."
	print "Finished Creating Queue"
