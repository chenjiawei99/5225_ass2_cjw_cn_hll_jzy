import boto3
import json
from boto3.dynamodb.conditions import Key
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Pics')

def lambda_handler(event, context):
    statusCode = 200
    headers = {'Content-Type': 'application/json'}
    try:
        if event['httpMethod'] == 'GET':
            if 'taskId' in event['pathParameters']:
                response = table.query(KeyConditionExpression=Key('id').eq(event['pathParameters']['taskId']))
                body = response['Items']
            else:
                response = table.scan()
                body = response['Items']
        elif event['httpMethod'] == 'POST':
            data1 = json.loads(event['body'])
            data={}
            data['tags'] = data1.get('tags', '')
            data['S3_url'] = data1.get('S3_url', '')
            data['id'] = context.aws_request_id
            data['updatedAt'] = int(datetime.now().timestamp() * 1000)
            table.put_item(Item=data)
            body = {'message': data}
            statusCode = 201
        elif event['httpMethod'] == 'PUT':
            data = json.loads(event['body'])
            table.update_item(Key={'id': data['id']}, UpdateExpression='SET #tags=:tags, #S3_url=:S3_url', ExpressionAttributeNames={'#tags': 'tags', '#S3_url': 'S3_url'}, ExpressionAttributeValues={':tags': data['tags'], ':S3_url': data['S3_url']})
            body = {'message': 'Item updated'}
        elif event['httpMethod'] == 'DELETE':
            data = json.loads(event['body'])
            table.delete_item(Key={'id': data['id']})
            body = {'message': 'Item deleted'}
        else:
            raise Exception(f'Unsupported method "{event["httpMethod"]}"')
    except Exception as e:
        statusCode = 400
        body = str(e)

    return {'statusCode': statusCode, 'body': body, 'headers': headers}