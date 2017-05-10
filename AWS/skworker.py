#!/usr/bin/python
import argparse
import os
import sys
import boto
import boto.sqs
from boto.sqs.message import Message
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import odd_point_star
import uuid
import time as tm
import boto.ec2



'''
    skworker.py
    
    Written By : Nicholas Neel

    Purpose : To continually run a program from a message queue continually. 
    For aws, create a sample instance configure to run this code at the start
    and then create an image of the sample instance.

        Then when requesting spot instances, use the sample instance image to distribute to 
    cluster nodes.

'''




if __name__ == "__main__":
	# Getting instance id and location
	#dic = boto.utils.get_instance_identity()['document']
	#REGION = str(dic[u'region'])
	#ID     = str(dic[u'instanceId'])
	
    # Obtain credential information
    aki        = open('/home/hollis/Documents/awsWebID.txt')
    ask        = open('/home/hollis/Documents/awsSecKey.txt')
    keyid      = aki.read().replace('\n','').replace(' ','')
    secret     = ask.read().replace('\n','').replace(' ','')
    region     = "us-east-1"
    queue_name = "StarData"



	# First, let's connect to the queue to get messages..
	sqsconn = boto.sqs.connect_to_region(region,aws_access_key_id=keyid,aws_secret_access_key=secret)

    # Memory storage login
	s3connection = S3Connection(aws_access_key_id=keyid,aws_secret_access_key=secret)

    # Get queue and bucket. NOTE you need to specify which queue if you are running more than one queue
	queue = sqsconn.get_all_queues()[0]
	bucket = s3connection.get_all_buckets()[0]

	# Now let's start the program...
	a = 1
	jobs_done = 0
	total_time = 0.0
	avg_time = 0.0

    # Main part of program to continue reading messages while there are still messages
	while a and queue.count() != 0:

        # Timer to keep track of stats in test running this code
		start = tm.time()
        # Hide the message this node took for 4000 ms and read its contents
		message = queue.get_messages(visibility_timeout = 4000)[0]
		
		print "message from queue downloaded"

        # open the b
		k = Key(bucket)

        # parse the body data
		body = str(message.get_body())
		mssg_parts = []
		b = 0
		for a in range(len(body)):
			if body[a] == ',':
				mssg_parts.append(body[b:a])
				b = a+1
			if a == len(body)-1:
				mssg_parts.append(body[b:a+1])


		key = Key
		bodyfile = ""
		homflies = []
		pd = []
		# Creating file to print homflies to...
		tempuuid = uuid.uuid4()
		
		dir_pd = mssg_parts[0]+"_pdstor/"
		dir_data = mssg_parts[0]+"_homflies/"

		name = str(tempuuid) + ".csv"

        # computes all homflies for the data points		
		print "computing homflies"
		for num in range(int(mssg_parts[1])):
			star = odd_point_star.odd_point_star(int(mssg_parts[0]))
			homflies.append(star.homfly())
			pd.append(star)

		print "Saving HOMFLY to file"
		bodyfile += str(len(homflies)) + "," + str(homflies).replace('[','').replace(']','')
		
        # Write a temporary file to upload to aws.
		tempfile = open(name,"a")
		tempfile.write(bodyfile)
		tempfile.close()
		full_name = dir_data + name
		key = boto.s3.key.Key(bucket,full_name)
		with open(name) as f:
			key.set_contents_from_file(f)

		os.remove(name)

        # Also saves the PDcode to files for future use.
		print "Saving PDCODEs to file"
		temp_pd_file = open(name,"a")
		for a in range(len(pd)):
			pd[a].write(temp_pd_file)
		full_name = dir_pd + str(tempuuid) + ".pdstor"
		key = boto.s3.key.Key(bucket,full_name)
		temp_pd_file.close()

		with open(name) as f:
			key.set_contents_from_file(f)
		os.remove(name)
		jobs_done += 1
		run_time = float((tm.time())-start)/60.0
		total_time += run_time

        # Print queue and time information
		print " "
		print "Number of jobs finished : ", jobs_done
		print "Number of jobs remaining :", queue.count()-1
		print "Time taken to complete in mins : ", run_time
		print "Average time                   : ", total_time/jobs_done
		
		print " " 
		queue.delete_message(message)
		print "deleted message"
		print " "
    
    # Delete instance when done? (not implemented yet, but could save a few pennies.)
	#ec2conn.stop_instances(instance_ids=[ID])
