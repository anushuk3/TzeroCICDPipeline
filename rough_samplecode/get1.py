import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    courId = event["courId"]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])

    if courId == "*":
        items = table.scan()
    else:
        items = table.query(
            KeyConditionExpression=Key('category').eq(courId)
        )

    return {"statusCode": 200, "body": items["Items"]}