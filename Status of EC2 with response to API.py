import json
import boto3

AWS_REGION = "ap-south-1"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
INSTANCE_ID = 'i-020f6c97dd2b339e8'

def mystatus():
    global instance_status
    
    instances = EC2_RESOURCE.instances.filter(
        InstanceIds=[
            INSTANCE_ID,
            ],
            )
    for instance in instances:
        print(f'Instance {instance.id} state is {instance.state["Name"]}')
        
        instance_status = {instance.state["Name"]}
        

def lambda_handler(event, context):
    mystatus()
    return json.loads(json.dumps(instance_status, default=str))
