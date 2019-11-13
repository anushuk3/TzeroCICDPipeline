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
        table = dynamodb.Table('Facultyprofile')
        response = table.scan()
        print('Total items in the table are ', response['Count'])
        for item in response['Items']:
            print(item)
        return response

    # Full table scan and fetch all the data
    fetch_all()
    faculty_data = fetch_all()
    return faculty_data