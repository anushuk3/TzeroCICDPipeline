#*********************************************************************************************************************
#Author – Anurag Shukla
#This script will operate on AWS DynamoDB to showcase various APIs
#*********************************************************************************************************************

import boto3
import json
from botocore.exceptions import ClientError

# Get the service resource on the cloud
#dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
# Get the service resource running on localhost; ensure you have the CLI done with the credentials file in .aws folder
# The nature of the credentials for localhost does not matter; type in any junk for accesskey and secret
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
#aws dynamodb describe-table --table-name anurag --endpoint-url http://localhost:8000 ( Listing the table)
# aws dynamodb describe-table --table-name anurag --endpoint-url http://localhost:8000 ( describe the table)
#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')

def lambda_handler(event, context):

    dynamodb = boto3.resource ('dynamodb', region_name='us-east-1')
    def create_table():
        print('\n*****************************create_table********************************************')
        print('Creating table CourseCatalog')
        try:
            table = dynamodb.create_table(
                # This is the table that we want to create
                TableName='CourseCatalog',
                # category is the PK ie hash and course is the sort key
                # these two together will uniquely identify a record/row
                KeySchema=[
                    {'AttributeName': 'category', 'KeyType': 'HASH'},
                    {'AttributeName': 'course', 'KeyType': 'RANGE'}
                ],
                # Specifying the data types for the PK and Sort keys respectively
                # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.DataTypes.html
                AttributeDefinitions=[
                    {'AttributeName': 'category', 'AttributeType': 'S'},
                    {'AttributeName': 'course', 'AttributeType': 'S'}
                ],
                # Planning for capacity units
                ProvisionedThroughput={ 'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1 }
            )
            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='CourseCatalog')
            print('DONE')

        except ClientError as e:
            print(' Skipped due to exception ', e.response['Error']['Code'])
            print(' Reason ', e.response['Error']['Message'])

    def insert_data(category, course, description, fee):
        print('\n*****************************insert_data********************************************')
        print('Inserting data in the table')
        # Instantiate a table resource object without actually creating a DynamoDB table.
        # Note that the attributes of this table are lazy-loaded: a request is not made nor are the attribute
        # values populated until the attributes on the table resource are accessed or its load() method is called.
        table = dynamodb.Table('CourseCatalog')
        table.put_item(
           Item={
                # The PK and the sort keys are mandatory
                'category': category,
                'course': course,
                # Due to the schemaless nature the following keys are not required in the table definition
                'description': description,
                'fee': fee,
            }
        )
        # Print out some data about the table.
        print ('Total items in the table are', table.item_count)

    def update_data(category, course, fee):
        print('\n*****************************update_data********************************************')
        print('Updating data in the table')
        table = dynamodb.Table('CourseCatalog')
        table.update_item(
            Key={
                'category': category,
                'course': course
            },
            UpdateExpression='SET fee = :val1',
            ExpressionAttributeValues={
                ':val1': fee
            }
        )
        print(' Done')

    def delete_data(category, course):
        print('\n*****************************delete_data********************************************')
        print('Deleting data in the table')
        table = dynamodb.Table('CourseCatalog')
        table.delete_item(
            Key={
                'category': category,
                'course': course
            }
        )
        print('Items left in the table are ', table.item_count)

    def main():
        #Create the table
        create_table()
        #Insert some sample data
        insert_data('Computer Science', 'CS00001', 'Computer Science CS00001', a)
        insert_data('Computer Science', 'CS00002', 'Computer Science CS00002', b)
        #Update a single record
        update_data('Computer Science', 'CS00002', 190000)
        delete_data('Computer Science', 'CS00001')
        #Insert some more data for a different partition
        insert_data('Data Science', 'DS00004', 'Data Science DS00004', c)
        insert_data('Data Science', 'DS00005', 'Data Science DS00005', d)
        insert_data('Data Science', 'DS00006', 'Data Science DS00006', e)
    main()
    return dict (
        statusCode=200,
        body=json.dumps (event)
    )
