import boto3

def send_plain_email():
    ses_client = boto3.client("ses", region_name="ap-south-1")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "chand.y@hcl.com",
            ],
            "CcAddresses": [
                "adityag@hcl.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Hello, from SES and Lambda - version2!",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Plain text email from Lambda and SES",
            },
        },
        Source="yogeshchand01@gmail.com",
    )
def lambda_handler(event, context):
    send_plain_email()