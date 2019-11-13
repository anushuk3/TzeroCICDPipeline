import boto3
import os

def lambda_handler(event, context):

    print ('Inserting data in the table')

    # Instantiate a table resource object without actually creating a DynamoDB table.
    # Note that the attributes of this table are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes on the table resource are accessed or its load() method is called.

    dynamodb = boto3.resource ('dynamodb')
    table = dynamodb.Table (os.environ['DB_TABLE_NAME'])
    table.put_item (
        Item={
            "category": "computer science",
            "course": "CS005",
            "description": "This computer science cs005",
            "fee": "600"
        }
    )
    print ('Total items in the table are', table.item_count)
    record = table.item_count
    return {"statusCode": 200, "body": record}