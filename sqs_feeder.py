#! /usr/bin/env python
import boto
import sys
from boto.sqs.message import Message
import connections

conn = connections.sqsconnect()

############ Command line argument. 
userinput = sys.argv[1]
#######################

#Getting list of all queues.
queues = conn.get_all_queues()
q = queues[0]

#Creating  message..
for i in range(1):
    m = Message()
    m.set_body(userinput)
    q.write(m)

print 'Message posted: '+ str(userinput)
