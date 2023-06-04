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
        if event['httpMethod'] == 'GET':
            if 'Tags' in event['pathParameters']:
                imageURL=[]
                Tags = event['pathParameters']['Tags']
                response = table.scan()
                data = response['Items']
                
                for index,element in enumerate(data):
                    url = element['S3_url']
                    tags = element['tags']
                    imageTagsInDB = set(tags)
                    quertTags = set(Tags)
                    
                    if len(Tags) == 0:
                        imageURL.append(url)
                    else:
                        if(quertTags == imageTagsInDB):
                           imageURL.append(url)
                           
                body = {"S3_urls": imageURL}

        else:
            raise Exception(f'Unsupported method "{event["httpMethod"]}"')
    except Exception as e:
        statusCode = 400
        body = str(e)

    return {'statusCode': statusCode, 'body': json.dumps(body, cls=DecimalEncoder), 'headers': headers}