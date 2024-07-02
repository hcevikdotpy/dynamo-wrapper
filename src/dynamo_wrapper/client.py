import boto3


class DynamoClient:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region):
        self.dynamodb = boto3.client('dynamodb',
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     region_name=region)

    def __getitem__(self, table_name):
        from .table import DynamoTable
        return DynamoTable(self.dynamodb, table_name)
