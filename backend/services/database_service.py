import boto3

# יצירת חיבור לטבלת DynamoDB שבה נשמרים הקישורים המקוצרים
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShortUrls')

def get_original_url(short_id):

    # מחזיר את הקישור המקורי על בסיס המזהה הקצר
    # מחזיר None אם המזהה לא נמצא

    try:
        response = table.get_item(Key={'id': short_id})
        
        if 'Item' in response:
            return response['Item']['url']
        return None
        
    except Exception as e:
        print(f"Database error in get_original_url: {str(e)}")
        raise e

def save_short_url(short_id, original_url):

    # שומר קישור מקוצר חדש במסד הנתונים
    # מחזיר True אם השמירה הצליחה, False אחרת

    try:
        table.put_item(Item={
            "id": short_id, 
            "url": original_url
        })
        return True
        
    except Exception as e:
        print(f"Database error in save_short_url: {str(e)}")
        return False

def url_exists(short_id):
    """
    בודק אם מזהה קצר כבר קיים במסד הנתונים
    שימושי למניעת התנגשויות
    """
    try:
        response = table.get_item(Key={'id': short_id})
        return 'Item' in response
        
    except Exception as e:
        print(f"Database error in url_exists: {str(e)}")
        return False