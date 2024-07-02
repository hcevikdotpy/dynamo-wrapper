import boto3
from boto3.dynamodb.conditions import Key, Attr
from .exceptions import ItemNotFoundError


class DynamoTable:
    def __init__(self, dynamodb, table_name):
        self.table = dynamodb.Table(table_name)

    def _format_condition(self, key, condition):
        if isinstance(condition, tuple) and len(condition) == 2:
            operator, value = condition
            if operator == 'EQ':
                return Attr(key).eq(value)
            elif operator == 'NE':
                return Attr(key).ne(value)
            elif operator == 'LT':
                return Attr(key).lt(value)
            elif operator == 'LTE':
                return Attr(key).lte(value)
            elif operator == 'GT':
                return Attr(key).gt(value)
            elif operator == 'GTE':
                return Attr(key).gte(value)
            elif operator == 'BETWEEN':
                return Attr(key).between(*value)
            elif operator == 'IN':
                return Attr(key).is_in(value)
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        raise ValueError("Invalid condition format. Expected a tuple (operator, value)")

    def _build_filter_expression(self, filter_conditions):
        if not filter_conditions:
            return None

        filter_expr = None
        for key, condition in filter_conditions.items():
            expr = self._format_condition(key, condition)
            filter_expr = expr if filter_expr is None else filter_expr & expr

        return filter_expr

    def find(self, filter_conditions=None):
        filter_expr = self._build_filter_expression(filter_conditions)

        response = self.table.scan(
            FilterExpression=filter_expr
        )

        return response.get('Items', [])

    def find_one(self, filter_conditions=None):
        filter_expr = self._build_filter_expression(filter_conditions)

        response = self.table.scan(
            FilterExpression=filter_expr
        )

        items = response.get('Items', [])
        return items[0] if items else None

    def delete_one(self, filter_conditions):
        key_condition = self._build_filter_expression(filter_conditions)
        response = self.table.delete_item(Key=key_condition)
        return response

    def count(self, filter_conditions=None):
        scan_kwargs = {'Select': 'COUNT'}
        if filter_conditions:
            scan_kwargs['FilterExpression'] = self._build_filter_expression(filter_conditions)

        response = self.table.scan(**scan_kwargs)
        count = response['Count']

        while 'LastEvaluatedKey' in response:
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = self.table.scan(**scan_kwargs)
            count += response['Count']

        return count

    def create_index(self, attribute_name, index_name=None):
        if index_name is None:
            index_name = f"{attribute_name}-index"

        response = self.dynamodb.update_table(
            TableName=self.table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': attribute_name,
                    'AttributeType': 'S'
                },
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    'Create': {
                        'IndexName': index_name,
                        'KeySchema': [
                            {
                                'AttributeName': attribute_name,
                                'KeyType': 'HASH'
                            },
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL',
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                },
            ],
        )
        return response
