# tests.py
from __future__ import print_function
import os
import unittest
import db
import boto3
import json
from botocore.vendored.requests.exceptions import ConnectionError
from botocore.exceptions import ClientError
from nikeyve import (status, create, retrieve,
    retrieve_all, update, delete)

TEST_TABLE = 'test-db'
os.environ['DYNAMO_TABLE'] = TEST_TABLE
os.environ['TEST'] = '1'

# NOTE: test require dynamoDB to be running locally
dynamo = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

TABLE_SCHEMA = { 
    'TableName': 'test-db',
    'AttributeDefinitions': [{'AttributeName': 'id',
                              'AttributeType': 'S'}],
    'KeySchema': [{'AttributeName': 'id',
                   'KeyType': 'HASH'}],
    'ProvisionedThroughput': {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    },

}

try:
    table = dynamo.Table(TEST_TABLE)
    table.delete()
except ConnectionError:
     raise Exception("Tests require that DynamoDB runs locally.")
except ClientError:
    # table is already deleted -- ignore
    pass 

class NiKeyVeTest(unittest.TestCase):

    def setUp(self):
        dynamo.create_table(**TABLE_SCHEMA)
        self.table = dynamo.Table(TEST_TABLE)

    def tearDown(self):
        self.table.delete()

    def test_create(self):
        event = {'pathParameters': {'id': 'key'},
                 'body': json.dumps({'data': 'value'})}
        context = {}
        create(event, context)
        result = retrieve(event, context)
        self.assertEqual(json.loads(result['body']), {'key': 'value'})

    def test_update(self):
        event = {'pathParameters': {'id': 'key'},
                 'body': json.dumps({'data': 123})}
        context = {}   
        create(event, context)
        event['body'] = json.dumps({'data': 321})
        result = update(event, context)
        self.assertEqual(json.loads(result['body']), {'key': 321})

    def test_delete(self):
        event = {'pathParameters': {'id': 'ten'},
                 'body': json.dumps({'data': 10})}
        context = {}
        create(event, context)
        del event['body']
        result = delete(event, context)
        self.assertIsNone(db.read(self.table, 'ten'))

    def test_retrieve_all(self):
        for i in range(10):
            event = {'pathParameters': {'id': str(i)},
                     'body': json.dumps({'data': i})}
            create(event, {})
        items = retrieve_all({}, {})
        # do a quick and dirty sort because table scans
        # are ordered by hash
        items = sorted(json.loads(items['body'])['keys'], 
        	           key=lambda d: int(list(d.keys()).pop()))
        for i, item in enumerate(items):
            key, value = str(i), item[str(i)]
            self.assertEqual(int(key), int(value))

if __name__ == '__main__':
    unittest.main()