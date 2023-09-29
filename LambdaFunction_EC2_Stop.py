# Version:05.07.22 F
# Author: Aditya
import boto3
import os

region=os.environ['REGION']
key=os.environ['KEY']
value=os.environ['VALUE']

def lambda_handler(event, context):
    ec2_resource = boto3.resource('ec2', region_name = region)
    running_filter = {'Name':'instance-state-name', 'Values':['running']}
    instances = ec2_resource.instances.filter(Filters=[running_filter])
    for instance in instances:
        if instance.tags !=None:
            
            for tag in instance.tags:
                
                if tag['Key']==key and tag['Value']==value :
                    instance.stop()
                    print("Instance stopped:",instance)
                