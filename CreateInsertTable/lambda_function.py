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
    #dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:8000')

    def create_table():
        print('\n*****************************create_table********************************************')
        print('Creating table CourseCatalog')
        try:
            table = dynamodb.create_table(
                # This is the table that we want to create
                TableName='CourseCatalog',
                # category is the PK ie hash and courseId is the sort key
                # these two together will uniquely identify a record/row
                KeySchema=[
                    {'AttributeName': 'category', 'KeyType': 'HASH'},
                    {'AttributeName': 'courseId', 'KeyType': 'RANGE'}
                ],
                # Specifying the data types for the PK and Sort keys respectively
                # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.DataTypes.html
                AttributeDefinitions=[
                    {'AttributeName': 'category', 'AttributeType': 'S'},
                    {'AttributeName': 'courseId', 'AttributeType': 'S'}
                ],
                # Planning for capacity units
                ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
            )
            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='CourseCatalog')
            print('DONE')
        except ClientError as e:
            print(' Skipped due to exception ', e.response['Error']['Code'])
            print(' Reason ', e.response['Error']['Message'])

    def insert_data(category, courseId, description, fee):
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
                'courseId': courseId,
                # Due to the schemaless nature the following keys are not required in the table definition
                'description': description,
                'fee': fee,
            }
        )
        # Print out some data about the table.
        # print('Total items in the table are', table.item_count)

    def update_data(category, courseId, fee):
        print('\n*****************************update_data********************************************')
        print('Updating data in the table')
        table = dynamodb.Table('CourseCatalog')
        table.update_item(
            Key={
                'category': category,
                'courseId': courseId
            },
            UpdateExpression='SET fee = :val1',
            ExpressionAttributeValues={
                ':val1': fee
            }
        )
        print(' Done')

    def delete_data(category, courseId):
        print('\n*****************************delete_data********************************************')
        print('Deleting data in the table')
        table = dynamodb.Table('CourseCatalog')
        table.delete_item(
            Key={
                'category': category,
                'courseId': courseId
            }
        )
        # print('Items left in the table are', table.item_count)


    # Create the table
    create_table()
    # Insert some sample data
    insert_data('Computer Science', 'Software Development','Specializations and courses in software development address the process of creating software, including development tools and methodologies (such as Agile development), programming languages (including Python, C, Java, and Scala), and software architecture and testing.', 11)
    insert_data('Computer Science', 'Mobile and Web Development','Mobile and web development courses will build your skills in creating web applications and native mobile apps for Android and iOS. Learn HTML/CSS and modern frameworks; PHP, JavaScript, Python, and other programming languages; and modern back-end technologies.', 12)
    insert_data('Computer Science', 'Algorithms', 'Algorithm courses develop your ability to articulate processes for solving problems and to implement those processes efficiently within software.learn to design algorithms for searching, sorting, and optimization and apply them to answer practical questions.', 13)
    # Update a single record
    update_data('Computer Science', 'Software Development', 13)
    insert_data('Information Technology', 'Cloud Computing', 'Cloud Computing courses and specializations teach cloud architecture, services, hosting, and more. Differentiate yourself in the IT industry, by learning how to properly leverage the Cloud.', 13)
    insert_data('Information Technology', 'Networking', 'Networking courses and specializations teach network administration, architecture, infrastructure, troubleshooting, and more. Break into the IT industry by learning applied networking skills.', 13)
    insert_data('Data Science', 'Data Analysis', 'Data analysis courses address methods for managing and analyzing large datasets. Start your career as a data scientist by studying data mining, big data applications, and data product development.', 14)
    insert_data('Data Science', 'Machine Learning', 'Machine learning courses focus on creating systems to utilize and learn from large sets of data. Topics of study include predictive algorithms, natural language processing, and statistical pattern recognition.', 15)
    insert_data('Data Science', 'Probability and Statistics','Probability and statistics courses teach skills in understanding whether data is meaningful, including optimization, inference, testing,and other methods for analyzing patterns in data and using them to predict, understand, and improve results.', 16)
    # Delete a record that exists
    # delete_data('Computer Science', 'Algorithms')
    # Insert some more data for a different partition

    return dict(
            statusCode=200,
            body=json.dumps(event)
    )

