#This Scripts creates a queue.

#! /usr/bin/env python
import boto
from boto.sqs.message import Message

#Connection conatins credentilas
import connections
workerfile = 'sqs_gworker2.py'

conn = connections.sqsconnect()

#Creating queue....
q = conn.get_queue('myque')

if q == None:
    q = conn.create_queue('myque',60)

print 'Queue created:' + str(q)

# Start default instance
fp  = open(workerfile)                                            
data = fp.read()                                                  
awsinst = connections.launchinst(1,data)                          
fp.close()                                  
print 'Default instance launched'
