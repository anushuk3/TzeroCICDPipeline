# *********************************************************************************************************************
# Author – Anurag Shukla
# This script will operate on AWS DynamoDB to showcase Getting an individual record from 
# the table based on the PK, Sort and PK+Sort keys
# *********************************************************************************************************************

import boto3
import json
from boto3.dynamodb.conditions import Key, Attr


# Get the service resource running on localhost; ensure you have the CLI done with the credentials file in .aws folder
# The nature of the credentials for localhost does not matter; type in any junk for accesskey and secret
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
# aws dynamodb describe-table --table-name anurag --endpoint-url http://localhost:8000 ( Listing the table)


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')
    def fetch_all():
        print('\n*****************************fetch_all********************************************')
        print('Getting all data from the table (not suited for production envs)')
        table = dynamodb.Table('CourseCatalog')
        response = table.scan()
        print('Total items in the table are ', response['Count'])
        for item in response['Items']:
            print(item)
        return response

    def fetch_pk(category):
        print('\n*****************************fetch_pk********************************************')
        print('Getting data from the table based on the PK')
        table = dynamodb.Table('CourseCatalog')
        # Different query conditions and select criteria are possible, an example is below
        # ProjectionExpression="#yr, title, info.genres, info.actors[0]",
        # ExpressionAttributeNames={ "#yr": "year" }, # Expression Attribute Names for Projection Expression only.
        # KeyConditionExpression=Key('year').eq(1992) & Key('title').between('A', 'L')
        response = table.query(
            KeyConditionExpression=Key('category').eq(category)
        )
        print(' Total items for this PK is ', response['Count'])
        for item in response['Items']:
            print(item)
        return response

    def fetch_data(category, courseId):
        print('\n*****************************fetch_data********************************************')
        print('Getting an individual record from the table based on the PK+Sort key')
        table = dynamodb.Table('CourseCatalog')
        response = table.get_item(
            Key={
                'category': category,
                'courseId': courseId
            }
        )
        try:
            item = response['Item']
            print(item)
        except Exception as e:
            print(' Either no data was returned or there was a problem')
            print(response)
        return response

    # Full table scan and fetch all the data
    fetch_all()
    fetchall = fetch_all()
    print("fetch_all from CourseCatalog", fetchall)
    # Get a single with PK and Sort
    fetch_data('Computer Science', 'Software Development')
    fetchdata = fetch_data('Computer Science', 'Software Development')
    print("fetch_pk from CourseCatalog", fetchdata)
    # Fetch based on only the partition key
    fetch_pk('Computer Science')
    fetchpk = fetch_pk("Computer Science")
    print("fetch_pk from CourseCatalog", fetchpk)

    # Fetch the complete data set
    # fetch_all()
    return fetchall
    # return dict {"statusCode": 200, "body": json.dumps (fetchall)}
