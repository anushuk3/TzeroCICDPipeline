import boto3
import json
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    courId = event["courId"]
    dynamodb = boto3.resource ('dynamodb', region_name='us-east-1')
    table = dynamodb.Table ('CourseCatalog')

    if courId == "*":
        items = table.scan ()
    else:
        items = table.query (
            KeyConditionExpression=Key ('category').eq (courId)
        )
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps ({'username': 'bob', 'id': 20})
    }
