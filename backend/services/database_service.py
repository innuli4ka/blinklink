import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShortUrls')

def get_original_url(short_id):
    try:
        response = table.get_item(Key={'id': short_id})
        
        if 'Item' in response:
            return response['Item']['url']
        return None
        
    except Exception as e:
        raise e

def save_short_url(short_id, original_url):
    try:
        table.put_item(Item={
            "id": short_id, 
            "url": original_url
        })
        return True
        
    except Exception as e:
        return False

def url_exists(short_id):
    try:
        response = table.get_item(Key={'id': short_id})
        return 'Item' in response
        
    except Exception as e:
        return False