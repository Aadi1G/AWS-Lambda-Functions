import json
import boto3

key ='ASG'
value = 'poc_autoscaling_start_stop'

AWS_REGION = "ap-south-1"


def mystatus2():
    
    global status
    
    client = boto3.client('rds', region_name=AWS_REGION)
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
