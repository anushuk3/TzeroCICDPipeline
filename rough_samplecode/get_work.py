import boto3
import json
from boto3.dynamodb.conditions import Key, Attr


# Get the service resource on the cloud
# dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
# Get the service resource running on localhost; ensure you have the CLI done with the credentials file in .aws folder
# The nature of the credentials for localhost does not matter; type in any junk for accesskey and secret
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
# aws dynamodb describe-table --table-name anurag --endpoint-url http://localhost:8000 ( describe the table)

def lambda_handler(event, context):
    # def fetch_all():
    print('\n*****************************fetch_all********************************************')
    print('Getting all data from the table (not suited for production envs)')
    courId = event["courId"]
    # dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('CourseCatalog')
    if courId == "*":
        response = table.scan()
        print('Total items in the table are ', response['Count'])
        for item in response['Items']:
            print(item)

    # def fetch_pk(category):
    else:
        print('\n*****************************fetch_pk********************************************')
        print('Getting data from the table based on the PK')
        # table = dynamodb.Table('CourseCatalog')
        response = table.query(
            KeyConditionExpression=Key('category').eq(courId)
        )
        print(' Total items for this PK is ', response['Count'])
        for item in response['Items']:
            print(item)
    return {"statusCode": 200, "body": response["Items"]}