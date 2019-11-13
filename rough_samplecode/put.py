import boto3
import os
import uuid
def lambda_handler(event, context):
    recordId = str(uuid.uuid4())

    print('Generating new DynamoDB record, with ID: ' + recordId)
    # Creating new record in DynamoDB table

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.put_item(
        Item={
            'category': recordId,
            'cat1': 'CS',
            'cat2': 'IT',
            'cat3': 'AS'
        }
    )
    return {"statusCode": 200, "body": recordId}