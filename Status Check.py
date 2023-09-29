#version: 16.10.2022 ver f 
#author : Aditya Garg

"""
uses following environment variables. Note these are case sensitive

 WHERE          Region name where resources are deployed
 KEY            TAG name on RDS instance to identify association with autoscaling group
 VALUE          Tag value on RDS instace to identify association with autoscaling group
 
"""

import json
import boto3
import os


where = os.environ['WHERE']
key = os.environ['KEY']
value = os.environ['VALUE']



def mystatus2():
    
    global status
    
    
    client = boto3.client('rds', region_name=where)
    response = client.describe_db_instances()
   
    for resp in response['DBInstances']:
        db_instance_arn = resp['DBInstanceArn']
        response = client.list_tags_for_resource(ResourceName=db_instance_arn)
   
        for tags in response['TagList']:
            if tags['Key'] == str(key) and tags['Value'] == str(value):
                status = resp['DBInstanceStatus']
                #InstanceID = resp['DBInstanceIdentifier']
                #print(InstanceID)
                #print(status)
            
    
def lambda_handler(event, context):
    mystatus2()
    return json.loads(json.dumps(status, default=str))
