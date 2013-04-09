#This script monitors the queue to scale up/down infrastrucure based on workload

#! /usr/bin/env python
import boto
from boto.sqs.message import Message
import time
import connections

UPPER_LIMIT=100
LOWER_LIMIT=100
SLEEP_TIME=2
instance_ids = []



conn = connections.sqsconnect()

while True:
    #Getting list of all queues.
    qs = conn.get_all_queues()
    count = qs[0].count()

    if count > UPPER_LIMIT:
        print 'Monitoring workers: Starting a new worker'
        fp  = open(workerfile)
        data = fp.read()
        awsinst = connections.launchinst(1,data)
        fp.close()
        instance_ids.append(awsinst.instances[0].id)
        #Waiting for instance to be in running state.
        while awsinst.instances[0].state!='running':
            time.sleep(1)
            count = qs[0].count()
            if count < UPPER_LIMIT:
                break
            awsinst.instances[0].update()
        print awsinst.instances[0].id
    elif count < UPPER_LIMIT:
        print 'Monitoring workers: Stopping a worker'
        if len(instance_ids) > 0:
            connections.terminateinst(instance_ids)
            #id = instance_ids.pop()
           # print id
        else:
            print 'Found no worker to stop'
    else:
        print 'Monitoring workers:'
    time.sleep(SLEEP_TIME)
 
   

