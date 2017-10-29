import os
import boto3
import json
import decimal

def get_db_connection():
    if 'TEST' in os.environ and os.environ['TEST'] == '1':
        dynamo = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    else:
        dynamo = boto3.resource('dynamodb')
    return dynamo.Table(os.environ['DYNAMO_TABLE'])

def write(db_connection, key, value):
    item = {'id': key,
            'value': value}
    if db_connection.put_item(Item=item):
        return True
    return False

def read(db_connection, key):
    item = db_connection.get_item(TableName=os.environ['DYNAMO_TABLE'],
                                  Key={'id': key})
    if 'Item' in item:
        return {
            item['Item']['id']: item['Item']['value']
        }
    else:
        return None

def read_all(db_connection):
    items = db_connection.scan()
    result = []
    for item in items['Items']:
        key, value = item['id'], item['value']
        result.append({key: value})
    return result

def delete(db_connection, key):
    db_connection.delete_item(Key={'id': key})
    return 