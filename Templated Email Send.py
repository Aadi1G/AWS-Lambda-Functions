import boto3

def sendemail():
    where = "ap-south-1"
    ses_client = boto3.client('ses',region_name=where)
    

    response = ses_client.send_templated_email(
        Source='yogeshchand01@gmail.com',
        Destination={
            'ToAddresses': ['adityag@hcl.com'],
            'CcAddresses': ['chand.y@hcl.com']
                    },
        ReplyToAddresses=['yogeshchand01@gmail.com'],
        Template='TestTemplate2',
        TemplateData='{"impactedUsername": "DummyUser"}'
        )

    print(response)
def lambda_handler(event,context):
    sendemail()