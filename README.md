# DynamoWrapper

DynamoWrapper is a Python library that provides a PyMongo-like interface for Amazon DynamoDB. It simplifies DynamoDB operations, making them more intuitive for developers familiar with MongoDB.

## Features

- PyMongo-like API for DynamoDB operations
- Simplified querying with a familiar syntax
- Easy table access and management
- Support for basic CRUD operations
- Index creation and management
- Batch operations support

## Installation

You can install DynamoWrapper using pip:
``pip install dynamo-wrapper``

## Quick Start

Here's a simple example to get you started:

```python
from dynamo_wrapper import DynamoClient

# Initialize the client
client = DynamoClient(aws_access_key_id, aws_secret_access_key, region)

# Access a table
table = client['my-table']

# Insert a document
table.insert_one({'id': '1', 'name': 'John Doe', 'age': 30})

# Find documents
results = table.find({'age': ('GT', 25)})

# Update a document
table.update_one({'id': ('EQ', '1')}, {'name': 'Jane Doe'})

# Delete a document
table.delete_one({'id': ('EQ', '1')})
```

## Usage

### Initializing the Client
```python
from dynamo_wrapper import DynamoClient

client = DynamoClient(aws_access_key_id, aws_secret_access_key, region)
```

### Accessing a Table
```python
table = client['table-name']
```

### Insert Operations
```python
# Insert one document
table.insert_one({'id': '1', 'name': 'John Doe', 'age': 30})

# Insert multiple documents
table.insert_many([
    {'id': '2', 'name': 'Jane Doe', 'age': 28},
    {'id': '3', 'name': 'Bob Smith', 'age': 35}
])
```

### Find Operations
```python
# Find one document
result = table.find_one({'id': ('EQ', '1')})

# Find multiple documents
results = table.find({'age': ('GT', 25)})

# Find with projection
results = table.find({'age': ('GT', 25)}, projection=['name', 'age'])

# Find with limit
results = table.find({'age': ('GT', 25)}, limit=10)
```

### Update Operations
```python
# Update one document
table.update_one({'id': ('EQ', '1')}, {'name': 'Jane Doe'})
```

### Delete Operations
```python
# Delete one document
table.delete_one({'id': ('EQ', '1')})
```

### Count Operations
```python
# Count documents
count = table.count({'age': ('GT', 25)})
```

### Index Operations
```python
# Create an index
table.create_index('name')
```

## Query Operators
DynamoWrapper supports the following comparison operators:
- ``EQ``: Equal to
- ``NE``: Not equal to
- ``LT``: Less than
- ``LTE``: Less than or equal to
- ``GT``: Greater than
- ``GTE``: Greater than or equal to
- ``IN``: In a list of values
- ``BETWEEN``: Between two values

Example:
```python
table.find({'age': ('GT', 25), 'status': ('EQ', 'active')})
```

## Error Handling
DynamoWrapper provides custom exceptions for various error scenarios. Here are some common exceptions:

- ``ItemNotFoundError``: Raised when an item is not found in the table
- ``QueryError``: Raised when there's an error in query formation or execution
- ``UpdateError``: Raised when an update operation fails
- ``DeleteError``: Raised when a delete operation fails
- ``InsertError``: Raised when an insert operation fails

Example:

```python
from dynamo_wrapper import ItemNotFoundError

try:
    result = table.find_one({'id': ('EQ', '999')})
except ItemNotFoundError:
    print("Item not found")
```

