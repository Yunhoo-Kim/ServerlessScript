import boto3
from botocore.exceptions import ClientError

def sendEmailHandler(event, context):
    client = boto3.client("ses", region_name="us-west-2")
    _to = event.get("ToAddresses", [])
    _type = event.get("_type", "html")
    subject = event.get("subject", "")
    body = {}
    if _type == "html"
        body = {
                "Html": {
                    "Charset": "UTF-8",
                    "Data": event.get("body")
                    }
                }
    try:
        response = client.send_email(
                Destination={
                    "ToAddresses" : _to,
                    },
                Message={
                    "Body": body,
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": subject
                        }
                    },
            Source="noreply@paytime.co.kr")
    except ClientError as e:
        print(e)
    else:
        print("success")

    return "success"
