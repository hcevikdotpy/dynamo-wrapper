"""
dynamo_wrapper - A PyMongo-like wrapper for DynamoDB
====================================================

This library provides a simplified interface for working with Amazon DynamoDB,
inspired by the PyMongo API. It aims to make DynamoDB operations more intuitive
for developers familiar with MongoDB.

Basic usage:
------------

    from dynamo_wrapper import DynamoClient

    client = DynamoClient(aws_access_key_id, aws_secret_access_key, region)
    table = client['my-table']

    # Find documents
    results = table.find({'status': ('EQ', 'active')})

    # Insert a document
    table.insert_one({'id': '1', 'name': 'John Doe'})

    # Update a document
    table.update_one({'id': ('EQ', '1')}, {'name': 'Jane Doe'})

For more information, please refer to the documentation.
"""

# Version of the dynamo_wrapper package
__version__ = "0.1.0"

# Import main classes and functions
from .client import DynamoClient
from .table import DynamoTable
from .exceptions import ItemNotFoundError

# Define what should be imported when using "from dynamo_wrapper import *"
__all__ = ['DynamoClient', 'DynamoTable', 'ItemNotFoundError']

# You can also add any initialization code here if needed

# For example, you might want to set up logging:
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

# Or you could set default configurations:
DEFAULT_REGION = 'us-west-2'

def set_default_region(region):
    global DEFAULT_REGION
    DEFAULT_REGION = region

# You could also include utility functions here:
def format_condition(condition):
    """Utility function to format filter conditions"""
    if isinstance(condition, tuple) and len(condition) == 2:
        return {'ComparisonOperator': condition[0], 'AttributeValueList': [condition[1]]}
    raise ValueError("Invalid condition format. Expected a tuple (operator, value)")

# Add any other initialization code or utility functions as needed