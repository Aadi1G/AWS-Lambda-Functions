#Version:
#Author: Aditya Garg

"""
uses following environment variables. Note these are case sensitive
 ASG_NAME       populate with name of autoscaling group
 DESIRED        Desired capacity of auto scaling group
 MIN            Minimum capacity of auto scaling group
 MAX            Maximum capacity of auto scaling group
 WHERE          Region name where resources are deployed
 KEY            TAG name on RDS instance to identify association with autoscaling group
 
"""

import boto3
import os
import sys
import time
from datetime import datetime, timezone
from time import gmtime, strftime

# describing env variable
where=os.environ['WHERE']
asg_name=os.environ['ASG_NAME']
min=int(os.environ['MIN'])
desired=int(os.environ['DESIRED'])
max=int(os.environ['MAX'])

# Boto Connection
asg = boto3.client('autoscaling', region_name=where)

def start_rds_all():
    where=os.environ['WHERE']
    key=os.environ['KEY']
    value=os.environ['ASG_NAME']
    client = boto3.client('rds', region_name=where)
    response = client.describe_db_instances()

    v_readReplica=[]
    for i in response['DBInstances']:
        readReplica=i['ReadReplicaDBInstanceIdentifiers']
        v_readReplica.extend(readReplica)
    
    for i in response['DBInstances']:

#The if condition below filters Read replicas.
            if i['DBInstanceIdentifier'] not in v_readReplica and len(i['ReadReplicaDBInstanceIdentifiers']) == 0:
                arn=i['DBInstanceArn']
                resp2=client.list_tags_for_resource(ResourceName=arn)
#check if the RDS instance is part of the required auto scaling group.
                if 0==len(resp2['TagList']):
                    print('DB Instance {0} is not associated with required auto scaling group'.format(i['DBInstanceIdentifier']))
                else:
                    for tag in resp2['TagList']:
                        if tag['Key']==key and tag['Value']==value:
                            if i['DBInstanceStatus'] == 'available':
                                print('{0} DB instance is already available'.format(i['DBInstanceIdentifier']))
                            elif i['DBInstanceStatus'] == 'stopped':
                                client.start_db_instance(DBInstanceIdentifier = i['DBInstanceIdentifier'])
                                print('Started DB Instance {0}'.format(i['DBInstanceIdentifier']))
                            elif i['DBInstanceStatus']=='starting':
                                print('DB Instance {0} is already in starting state'.format(i['DBInstanceIdentifier']))
                            elif i['DBInstanceStatus']=='stopping':
                                print('DB Instance {0} is in stopping state. Please wait before starting'.format(i['DBInstanceIdentifier']))
                        elif tag['Key']!=key and tag['Value']!=value:
                            print('DB instance {0} is not associated with required auto scaling group'.format(i['DBInstanceIdentifier']))
                        elif len(tag['Key']) == 0 or len(tag['Value']) == 0:
                            print('DB Instance {0} is not associated with required auto scaling group'.format(i['DBInstanceIdentifier']))
            elif i['DBInstanceIdentifier'] in v_readReplica:
                print('DB Instance {0} is a Read Replica.'.format(i['DBInstanceIdentifier']))
            else:
                print('DB Instance {0} has a read replica. Cannot shutdown & start a database with Read Replica'.format(i['DBInstanceIdentifier']))

def lambda_handler(event, context):
  response = asg.update_auto_scaling_group(AutoScalingGroupName=asg_name, MinSize=min, DesiredCapacity=desired, MaxSize=max)  
  start_rds_all()