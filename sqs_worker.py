#! /usr/bin/env python
import os
import sys
import csv
import time
import json
import urllib2
import random
from datetime import datetime

from boto.s3.key import Key
from boto.sqs.message import Message

#############################################################################
from boto.sqs.connection import SQSConnection
from boto.ec2.connection import EC2Connection
from boto.s3.connection import S3Connection

aws_id = ''
aws_secret = ''
conn = []

def sqsconnect():
    conn = SQSConnection(aws_id,aws_secret)
    return conn

def s3connect():
    conn = S3Connection(aws_id, aws_secret)
    return conn

def launchinst(count,data):
    global conn
    conn=EC2Connection(aws_id,aws_secret)
    awsinst= conn.run_instances(image_id='ami-0078da69',max_count=count,user_data=data)
    return awsinst
    
def terminateinst(inst_id):
    conn.terminate_instances(instance_ids=[inst_id])

###################################################################################
#Creating SQS connection
sqsconn = sqsconnect()

#Creating S3 Connection
s3conn = s3connect()


log_bucket='sqs.log'
result_bucket='sqs1.res'
output_file='output'
log_file='logs'
###########################

input_bucket_name='sqs.input'
input_file = 'data.csv'
app_bucket_name = 'app_type'
api_file = 'workdefinition.csv'
# Retrieve message
queues = sqsconn.get_all_queues()
q =  queues[0]
while True:
    messages = q.get_messages()
    if len(messages) <= 0:
        sys.exit()
     #   time.sleep(15)
     #   continue
    msg = messages[0]
    msgbody = msg.get_body()
    # Retrieve the argument data from S3
    msgtype = msgbody[0:2]
    apitype = msgbody[2:5]
    rowid = msgbody[5:]
    print msgtype,input_bucket_name,input_file,apitype,rowid
    if (msgtype == '') or (input_bucket_name == '')  or (input_file == '')  or (rowid == '') or (apitype == ''):
        print 'Invalid input'
        sys.exit()
    #Getting api type from bucket
    app_bucket = s3conn.get_bucket(app_bucket_name)
    k= Key(app_bucket)
    k.key=api_file
    if k.exists():
        data=k.get_contents_as_string()
        dict_file = open("api.csv", "w")
        dict_file.write(data)
        dict_file.close()
    else:
        print 'work definition file not found'
        sys.exit()

    reader = csv.reader(open('api.csv', 'rb'))
    mydict = dict(x for x in reader)

    argdata1 = mydict[apitype]
    print apitype,argdata1
    os.remove('api.csv')
    #Getting input data from bucket
    input_bucket = s3conn.get_bucket(input_bucket_name)
    k= Key(input_bucket)
    k.key=input_file
    if k.exists():
        data=k.get_contents_as_string()
        dict_file = open("dict.csv", "w")
        dict_file.write(data)
        dict_file.close()
    else:
        print 'input file not found'
        sys.exit()

    reader = csv.reader(open('dict.csv', 'rb'))
    mydict = dict(x for x in reader)

    argdata2 = mydict[rowid]
    print rowid,argdata2
    os.remove('dict.csv')

    # Log message in the beginning of processing
    msgdetails = 'processing started '+ str(msg) + '\t ' + str(datetime.now())  
    bucket = s3conn.get_bucket(log_bucket)
    k= Key(bucket)
    k.key=log_file
    if k.exists():
        prev_data=k.get_contents_as_string()
    else:
        prev_data = ''
    msgdetails = prev_data + '\n' + msgdetails
    k.set_contents_from_string(msgdetails)

    # Get message type
    app_bucket = s3conn.get_bucket('app_type')
    k= Key(app_bucket)
    k.key='app_type.csv'
    if k.exists():
        data=k.get_contents_as_string()
        dict_file = open("app_type.csv", "w")
        dict_file.write(data)
        dict_file.close()
    else:
        print 'app types file not found'
        sys.exit()

    reader = csv.reader(open('app_type.csv', 'rb'))
    appdict = dict(x for x in reader)
    apptype = appdict[msgtype]
    print apptype

    # Download the app if it does not exist already
    if os.path.isfile(apptype+'.py'):
        print 'app found'
    else:
        # Downlod the app
        k.key=apptype+'.py'
        if k.exists():
            data=k.get_contents_as_string()
            app_file = open(k.key, "w")
            app_file.write(data)
            app_file.close()
        else:
            print 'app not found in S3'
            sys.exit()

    # Process the message using the app
    r = str(random.randint(1000000,99999999999999))
    argdata = 'file'+r+','+str(argdata1)+','+str(argdata2)
    os.system('chmod a+x '+ apptype +'.py')
    os.system('./'+ apptype +'.py' + '  '+ argdata)

    print 'Storing message result in S3'

    # Store the result in S3
    bucket = s3conn.get_bucket(result_bucket)
    k= Key(bucket)
    k.key=output_file
    if k.exists():
        prev_data=k.get_contents_as_string()
    else:
        prev_data = ''


    fs = open('file'+r,'a')
    fs.write(prev_data)
    fs.close()

    k.set_contents_from_filename('file'+r)
    q.delete_message(msg)

    # Log message in the end of processing
    msgdetails = 'processing finished '+ str(msg) + '\t ' + str(datetime.now())
    bucket = s3conn.get_bucket(log_bucket)
    k= Key(bucket)
    k.key=log_file
    if k.exists():
        prev_data=k.get_contents_as_string()
    else:
        prev_data = ''
    msgdetails = prev_data + '\n' + msgdetails
    k.set_contents_from_string(msgdetails)
    os.remove('file'+r)
