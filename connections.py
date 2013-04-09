import boto
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
    conn.terminate_instances(instance_ids=inst_id)
