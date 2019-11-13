#*********************************************************************************************************************
#Author – Anurag Shukla
#This script will operate on AWS DynamoDB to Create Table
#*********************************************************************************************************************

import boto3
from botocore.exceptions import ClientError

# Get the service resource on the cloud
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
# Get the service resource running on localhost; ensure you have the CLI done with the credentials file in .aws folder
# The nature of the credentials for localhost does not matter; type in any junk for accesskey and secret
# java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
#aws dynamodb describe-table --table-name anurag --endpoint-url http://localhost:8000 ( Listing the table)
# aws dynamodb describe-table --table-name anurag --endpoint-url http://localhost:8000 ( describe the table)
#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')

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

def main():
    #Create the table
    create_table()
main ()
