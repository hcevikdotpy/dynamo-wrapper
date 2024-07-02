class DynamoWrapperException(Exception):
    """Base exception class for DynamoWrapper"""
    pass


class ConnectionError(DynamoWrapperException):
    """Raised when there's an issue connecting to DynamoDB"""
    pass


class ConfigurationError(DynamoWrapperException):
    """Raised when there's a configuration issue"""
    pass


class TableNotFoundError(DynamoWrapperException):
    """Raised when attempting to operate on a non-existent table"""
    pass


class ItemNotFoundError(DynamoWrapperException):
    """Raised when an item is not found in the table"""
    pass


class ValidationError(DynamoWrapperException):
    """Raised when there's a data validation error"""
    pass


class QueryError(DynamoWrapperException):
    """Raised when there's an error in query formation or execution"""
    pass


class UpdateError(DynamoWrapperException):
    """Raised when an update operation fails"""
    pass


class DeleteError(DynamoWrapperException):
    """Raised when a delete operation fails"""
    pass


class InsertError(DynamoWrapperException):
    """Raised when an insert operation fails"""
    pass


class IndexError(DynamoWrapperException):
    """Raised when there's an issue with indexes"""
    pass


class CapacityExceededError(DynamoWrapperException):
    """Raised when DynamoDB's capacity is exceeded"""
    pass


class TransactionError(DynamoWrapperException):
    """Raised when a transaction fails"""
    pass


class ConditionCheckFailedError(DynamoWrapperException):
    """Raised when a condition check fails during an operation"""
    pass


class ResourceInUseError(DynamoWrapperException):
    """Raised when attempting to create a table that already exists"""
    pass


class ResourceNotFoundError(DynamoWrapperException):
    """Raised when a requested resource is not found"""
    pass


class ThrottlingError(DynamoWrapperException):
    """Raised when requests are being throttled by DynamoDB"""
    pass


class LimitExceededError(DynamoWrapperException):
    """Raised when a limit (e.g., max number of tables) is exceeded"""
    pass


class ProvisionedThroughputExceededError(DynamoWrapperException):
    """Raised when the provisioned throughput is exceeded"""
    pass


class ConditionalCheckFailedException(DynamoWrapperException):
    """Raised when a conditional check fails during an operation"""
    pass


class BatchWriteError(DynamoWrapperException):
    """Raised when there's an error during a batch write operation"""
    pass


class SerializationError(DynamoWrapperException):
    """Raised when there's an error serializing data for DynamoDB"""
    pass


class DeserializationError(DynamoWrapperException):
    """Raised when there's an error deserializing data from DynamoDB"""
    pass