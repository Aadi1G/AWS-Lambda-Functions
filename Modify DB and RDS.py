#function Pupose: To change the instance types for both RDS and EC2

'''
How it works:
Pass on the below listed parameters as Environment Variable. For these env variables
the required action will be performed

WHERE: Region where the resources are located
DBIdentifier : Identifier of DB which needs to be modified
DBClass : new class of DB as desired
EC2InstanceID : ID of the EC2 instance which needs to be modifier
EC2InstanceType : new type of the instance
'''

import json
import boto3
import os
import time

where=os.environ['WHERE']
dbidentifier =os.environ['DBIdentifier']
dbclass =os.environ['DBClass']
instanceid =os.environ['EC2InstanceID']
newistanceType=os.environ['EC2InstanceType']

def lambda_handler(event, context):
    #modifying the DB instance. Change will be applied immidiately
    client = boto3.client('rds', region_name=where)
    response = client.modify_db_instance(DBInstanceIdentifier=dbidentifier, DBInstanceClass=dbclass, ApplyImmediately=True)
    
    #modifying EC2 instance. 3step process - Stop, modify the instance, start the instance
    ec2_client = boto3.client('ec2', region_name = where)
    ec2_stop = ec2_client.stop_instances(InstanceIds=instanceid.split()) #using split function to convert string to list
    time.sleep(45) # waiting for 45 seconds for instance to stop
    ec2_response = ec2_client.modify_instance_attribute(InstanceId=instanceid, Attribute='instanceType', Value=newistanceType)
    ec2_start=ec2_client.start_instances(InstanceIds=instanceid.split()) #using split function to convert string to list