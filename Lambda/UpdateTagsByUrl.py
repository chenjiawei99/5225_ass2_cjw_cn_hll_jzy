import boto3
import json
from boto3.dynamodb.conditions import Key
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Pics')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    statusCode = 200
    headers = {'Content-Type': 'application/json'}
    try:
        if event['httpMethod'] == 'PUT' :
            if 's3_url' in event['pathParameters']:
                data = json.loads(event['body'])
                table.update_item(Key={'S3_url': event['pathParameters']['s3_url']}, UpdateExpression='SET tags=:tags', ExpressionAttributeValues={':tags': data['tags']})
                body = {'message': 'Item updated'}


        else:
            raise Exception(f'Unsupported method "{event["httpMethod"]}"')
    except Exception as e:
        statusCode = 400
        body = str(e)

    return {'statusCode': statusCode, 'body': json.dumps(body, cls=DecimalEncoder), 'headers': headers}