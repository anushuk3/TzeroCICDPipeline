# *********************************************************************************************************************
# Author – Anurag Shukla
# This script will operate on AWS DynamoDB to showcase create table, insert data, update data and delete data
# *********************************************************************************************************************

import boto3
import json
from botocore.exceptions import ClientError


# Get the service resource on the cloud
# dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
# Get the service resource running on localhost; ensure you have the CLI done with the credentials file in .aws folder
# The nature of the credentials for localhost does not matter; type in any junk for accesskey and secret
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
# aws dynamodb describe-table --table-name anurag --endpoint-url http://localhost:8000 ( Listing the table)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')

    def create_table():
        print('\n*****************************create_table********************************************')
        print('Creating table Facultyprofile')
        try:
            table = dynamodb.create_table(
                # This is the table that we want to create
                TableName='Facultyprofile',
                # Name is the PK ie hash and courses is the sort key
                # these two together will uniquely identify a record/row
                KeySchema=[
                    {'AttributeName': 'Name', 'KeyType': 'HASH'},
                    {'AttributeName': 'courses', 'KeyType': 'RANGE'}
                ],
                # Specifying the data types for the PK and Sort keys respectively
                # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.DataTypes.html
                AttributeDefinitions=[
                    {'AttributeName': 'Name', 'AttributeType': 'S'},
                    {'AttributeName': 'courses', 'AttributeType': 'S'}
                ],
                # Planning for capacity units
                ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
            )
            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='Facultyprofile')
            print('DONE')
        except ClientError as e:
            print(' Skipped due to exception ', e.response['Error']['Code'])
            print(' Reason ', e.response['Error']['Message'])

    def insert_data(Name, courses, about):
        print('\n*****************************insert_data********************************************')
        print('Inserting data in the table')
        # Instantiate a table resource object without actually creating a DynamoDB table.
        # Note that the attributes of this table are lazy-loaded: a request is not made nor are the attribute
        # values populated until the attributes on the table resource are accessed or its load() method is called.
        table = dynamodb.Table('Facultyprofile')
        table.put_item(
            Item={
                # The PK and the sort keys are mandatory
                'Name': Name,
                'courses': courses,
                # Due to the schemaless nature the following keys are not required in the table definition
                'about': about,
            }
        )
        # Print out some data about the table.
        # print('Total items in the table are', table.item_count)

    # Create the table
    create_table()
    # Insert some sample data
    insert_data('Nirmallya', 'Computer Science', 'great learning faculty')
    insert_data('Anurag', 'Data Science', 'great learning faculty')
    insert_data('Pankaj', 'Information Technology', 'great learning faculty')
    insert_data('Vipin', 'Data Science', 'great learning faculty')
    insert_data('Deepak', 'Data Science', 'great learning faculty')
    insert_data('Akshat', 'Data Science', 'great learning faculty')
    insert_data('Vimal', 'Data Science', 'great learning faculty')

    return dict(
        statusCode=200,
        body=json.dumps(event)
    )