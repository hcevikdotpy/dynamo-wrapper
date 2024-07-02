import pytest
from moto import mock_dynamodb
import boto3
from dynamo_wrapper import DynamoClient, ItemNotFoundError, QueryError


# Setup for mocking DynamoDB
@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def dynamodb(aws_credentials):
    with mock_dynamodb():
        yield boto3.client('dynamodb', region_name='us-east-1')


@pytest.fixture(scope='function')
def dynamo_client(dynamodb):
    return DynamoClient('testing', 'testing', 'us-east-1')


@pytest.fixture(scope='function')
def test_table(dynamodb):
    dynamodb.create_table(
        TableName='test-table',
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    return 'test-table'


def test_insert_one(dynamo_client, test_table):
    table = dynamo_client[test_table]
    item = {'id': '1', 'name': 'John Doe', 'age': 30}
    response = table.insert_one(item)
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200


def test_find_one(dynamo_client, test_table):
    table = dynamo_client[test_table]
    item = {'id': '1', 'name': 'John Doe', 'age': 30}
    table.insert_one(item)

    result = table.find_one({'id': ('EQ', '1')})
    assert result == item


def test_find_one_not_found(dynamo_client, test_table):
    table = dynamo_client[test_table]
    with pytest.raises(ItemNotFoundError):
        table.find_one({'id': ('EQ', '999')})


def test_update_one(dynamo_client, test_table):
    table = dynamo_client[test_table]
    item = {'id': '1', 'name': 'John Doe', 'age': 30}
    table.insert_one(item)

    update_response = table.update_one({'id': ('EQ', '1')}, {'name': 'Jane Doe', 'age': 31})
    assert update_response['ResponseMetadata']['HTTPStatusCode'] == 200

    updated_item = table.find_one({'id': ('EQ', '1')})
    assert updated_item['name'] == 'Jane Doe'
    assert updated_item['age'] == 31


def test_delete_one(dynamo_client, test_table):
    table = dynamo_client[test_table]
    item = {'id': '1', 'name': 'John Doe', 'age': 30}
    table.insert_one(item)

    delete_response = table.delete_one({'id': ('EQ', '1')})
    assert delete_response['ResponseMetadata']['HTTPStatusCode'] == 200

    with pytest.raises(ItemNotFoundError):
        table.find_one({'id': ('EQ', '1')})


def test_find(dynamo_client, test_table):
    table = dynamo_client[test_table]
    items = [
        {'id': '1', 'name': 'John Doe', 'age': 30},
        {'id': '2', 'name': 'Jane Doe', 'age': 28},
        {'id': '3', 'name': 'Bob Smith', 'age': 35},
    ]
    for item in items:
        table.insert_one(item)

    results = table.find({'age': ('GT', 29)})
    assert len(results) == 2
    assert any(item['name'] == 'John Doe' for item in results)
    assert any(item['name'] == 'Bob Smith' for item in results)


def test_count(dynamo_client, test_table):
    table = dynamo_client[test_table]
    items = [
        {'id': '1', 'name': 'John Doe', 'age': 30},
        {'id': '2', 'name': 'Jane Doe', 'age': 28},
        {'id': '3', 'name': 'Bob Smith', 'age': 35},
    ]
    for item in items:
        table.insert_one(item)

    count = table.count({'age': ('GT', 29)})
    assert count == 2


def test_create_index(dynamo_client, test_table):
    table = dynamo_client[test_table]
    response = table.create_index('name')
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    # Check if the index was created
    table_description = dynamo_client.dynamodb.describe_table(TableName=test_table)
    gsi = table_description['Table']['GlobalSecondaryIndexes']
    assert len(gsi) == 1
    assert gsi[0]['IndexName'] == 'name-index'

