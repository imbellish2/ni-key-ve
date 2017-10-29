from __future__ import print_function
import os
import json
import logging
import boto3 
import db
from utils import undecimalify

log = logging.getLogger()
log.setLevel(logging.DEBUG)

@undecimalify
def status(event, context):
    log.info('GET to /status/')
    body = {
        'statusCode': 200,
        'body': {'status': 'OK'}
    }
    return body

@undecimalify
def create(event, context):
    log.info('POST to /create/')
    key = event['pathParameters']['id']
    value = json.loads(event['body'])
    if 'data' not in value:
        raise Exception('Missing parameter: data')

    db_connection = db.get_db_connection()
    if db.write(db_connection, key, value['data']):
        value = db.read(db_connection, key)
        
        return {
            'statusCode': 200,
            'body': value
        }
    else:
        return {
            'statusCode': 500,
            'body': {'error': 'Failed to create %s' % key}
        }

@undecimalify
def retrieve(event, context):
    log.info('GET to retrieve')
    key = event['pathParameters']['id']
    db_connection = db.get_db_connection()
    value = db.read(db_connection, key)
    
    if value is not None:
        return {
            'statusCode': 200,
            'body': value
        }
    else:
        return {
            'statusCode': 404,
            'body': {'error': 'Not found'}
        }

@undecimalify
def retrieve_all(event, context):
    log.info('GET to retrive_all')
    db_connection = db.get_db_connection()

    response = {
        'statusCode': 200,
        'body': {'keys': db.read_all(db_connection)}
    }
    
    return response

@undecimalify
def update(event, context):
    log.info('PUT to update')
    db_connection = db.get_db_connection()
    key = event['pathParameters']['id']
    value = json.loads(event['body'])
    if 'data' not in value:
        raise Exception('Missing parameter: data')
    if not db.read(db_connection, key):
        response = {
            'statusCode': 404,
            'body': {'error': 'Not found'}
        }
    elif db.write(db_connection, key, value['data']):
        read = db.read(db_connection, key)
        response = {
            'statusCode': 200,
            'body': read
        }
    
    return response

@undecimalify
def delete(event, context):
    log.info('DELETE to delete')
    db_connection = db.get_db_connection()
    key = event['pathParameters']['id']
    db.delete(db_connection, key)

    return {
        'statusCode': 200
    }
