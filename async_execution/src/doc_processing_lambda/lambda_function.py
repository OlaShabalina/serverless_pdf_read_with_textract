import json
import boto3
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)


sns = boto3.client('sns')
textract = boto3.client('textract')


def handler(event, context):
    topic_arn = os.environ['TEXTRACT_NOTIFICATION_TOPIC']
    textract_role = os.environ['TEXTRACT_ROLE_ARN']

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        try:
            # Start Textract asynchronous processing
            response = textract.start_document_text_detection(
                DocumentLocation={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                },
                NotificationChannel={
                    'SNSTopicArn': topic_arn,  # Your SNS topic ARN
                    'RoleArn': textract_role  # The ARN of the IAM role with SNS publish permissions
                }
            )

            logger.info(f"File {key} is sent to Textract!")

        except Exception as e:
            logger.error(f"Error processing file {key} from bucket {bucket}: {str(e)}")
            continue

    return {
        'statusCode': 200,
        'body': 'Textract processing initiation complete!'
    }
