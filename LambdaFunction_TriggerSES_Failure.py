#version 1.0.15Dec2022
#Author: Aditya Garg
#Owner: ROAR DevOps Team
# works with HTTP API from API gateway

#importing required libraries

import json
import boto3
import os
from datetime import datetime  
import dateutil.tz

# define Environment Variable for region where SES is depoyed and Source email ID
# which is used by SES

WHERE = os.environ['REGION']
senderEmailID =os.environ['SENDER']

#setting up timezone for timestamps
tz=dateutil.tz.gettz('Asia/Kolkata')

# defining labda event and context

def lambda_handler(event, context):
    ses_client = boto3.client('ses',region_name=WHERE)
    #print ("request Received")
    print(event)  # printing the information received from API call. The details will be available in cloudwatch
    
    #accepting inputs from the API body and storing in variables
         # creating dictionary  in json format from the body of the API. ref. row#22
    decodedBody = json.loads(event['body'])  # 
         
         #filtering out the information required for sending the notification 
    TjobName = decodedBody['jobName']
    TcompanyName = decodedBody['companyName']
    TclassName = decodedBody['className']
    TimpactedUsername = decodedBody ['impactedUsername']
    TjobStartTime = decodedBody['jobStartTime']
    #TjobCompletionTime = decodedBody['jobCompletionTime']
    TjobID = decodedBody['jobID']
    TjobType = decodedBody['jobType']
    TinstanceURL = decodedBody ['instanceURL']
    TemailTo = decodedBody['emailTo']
    TemailBcc = decodedBody ['emailBcc']
    
    #setting up email body
    CHARSET = "UTF-8"
    #senderEmailID ="yogeshchand01@gmail.com"
    subj = "ROAR | {} stage failed | Company: {} | Class: {}".format(TjobName,TcompanyName,TclassName)
    
    HTML_EMAIL_CONTENT = """
        <html>
            <head></head>
            <h1 style='text-align:center'></h1>
            <p>Dear {},<br><br>The <b> {} </b> stage initiated by you did not complete successfully. 
             Below are the details of executed stage:<br><br>
             <b>Company:</b> {}<br>
             <b>Start Time:</b> {}<br>
             <b>Class:</b> {}<br>
             <b>Job ID:</b> {}<br>
             <b>Data Processing Type:</b> {}<br>
             <b>Instance:</b> {}<br><br>
             For more details, you may visit Processing History 
             tab in \"Job History & Reports\" section within ROAR application.<br><br> 
             In case you want to report an issue with this execution, please log a 
             ticket via our  <a href='https://support.dryice.ai'>Product Support Portal</a> 
             quoting Job ID.<br><br></p> 
            </body>
            <table class="Table" style="width:200.0%">
	        <tbody>
		    <tr>
			<td style="background-color:#336699">
			<p style="text-align:center"><span style="font-size:11pt">
			<span style="font-family:Calibri,sans-serif"><span style="font-size:7.5pt">
			<span style="font-family:&quot;Verdana&quot;,sans-serif">
			<span style="color:white">
			Note: This is a system generated e-mail  sent from a mailbox which is not monitored. 
			Please <b>DO NOT</b> reply to this e-mail.</span></span></span></span></span></p>
			</td>
		    </tr>
	        </tbody>
            </table>    
        </html>
    """
    # setting up SES code
    
    #try sending email notification
    try:
        response = ses_client.send_email(
            Destination={
                "ToAddresses": [
                    TemailTo,
                ],
                "BccAddresses": [
                    TemailBcc,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": HTML_EMAIL_CONTENT.format(TimpactedUsername,TjobName,TcompanyName,TjobStartTime,TclassName,TjobID,TjobType,TinstanceURL),
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": subj
                },
            },
            Source=senderEmailID,
        )
    # Capture and display  error if something goes wrong.	
    except ClientError as e:
        print(response['MessageId'])   #printing message ID.Visible in Cloudwatch
        print("Failed Delivery. "+e.response['Error']['Message']) #printing error message. Visible in Cloudwatch
        print(response)
        return {"status":"Notification Failed at "++datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S") +" IST with error message: "+e.response['Error']['Message'],
                "Message ID": response['MessageId'] 
        }
    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])
        return {"status":"Successfully sent notification at "+datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S") +" IST. Message ID is: "+response['MessageId']
        }