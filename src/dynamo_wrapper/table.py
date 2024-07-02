import boto3
from boto3.dynamodb.conditions import Key, Attr
from .exceptions import ItemNotFoundError


class DynamoTable:
    def __init__(self, dynamodb, table_name):
        self.dynamodb = dynamodb
        self.table_name = table_name
        self.table = self.dynamodb.Table(table_name)

    def _format_condition(self, condition):
        if isinstance(condition, tuple) and len(condition) == 2:
            operator, value = condition
            if operator == 'EQ':
                return Attr(Key) == value
            elif operator == 'NE':
                return Attr(Key) != value
            elif operator == 'LT':
                return Attr(Key) < value
            elif operator == 'LTE':
                return Attr(Key) <= value
            elif operator == 'GT':
                return Attr(Key) > value
            elif operator == 'GTE':
                return Attr(Key) >= value
            elif operator == 'IN':
                return Attr(Key).is_in(value)
            elif operator == 'BETWEEN':
                return Attr(Key).between(*value)
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

    def find(self, filter_conditions=None, projection=None, limit=None):
        scan_kwargs = {}

        if filter_conditions:
            scan_kwargs['FilterExpression'] = self._build_filter_expression(filter_conditions)

        if projection:
            scan_kwargs['ProjectionExpression'] = ','.join(projection)

        if limit:
            scan_kwargs['Limit'] = limit

        response = self.table.scan(**scan_kwargs)
        items = response.get('Items', [])

        while 'LastEvaluatedKey' in response:
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = self.table.scan(**scan_kwargs)
            items.extend(response.get('Items', []))

        return items

    def find_one(self, filter_conditions=None):
        results = self.find(filter_conditions, limit=1)
        if results:
            return results[0]
        raise ItemNotFoundError("No matching item found")

    def insert_one(self, item):
        response = self.table.put_item(Item=item)
        return response

    def insert_many(self, items):
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    def update_one(self, filter_conditions, update_values):
        key_condition = self._build_filter_expression(filter_conditions)

        update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in update_values.keys())
        expression_attribute_names = {f"#{k}": k for k in update_values.keys()}
        expression_attribute_values = {f":{k}": v for k, v in update_values.items()}

        response = self.table.update_item(
            Key=key_condition,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

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