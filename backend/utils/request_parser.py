def determine_request_method(event):

    # קובע את סוג הבקשה (GET או POST) בהתאם לפורמט של AWS API Gateway
    # תומך גם ב-API Gateway v1 וגם ב-v2

    # בדיקה לפורמט של API Gateway v1
    if 'httpMethod' in event:
        return event['httpMethod']
    
    # בדיקה לפורמט של API Gateway v2
    if 'requestContext' in event and 'http' in event['requestContext']:
        return event['requestContext']['http'].get('method')
    
    return None

def extract_path_parameter(event):

    # מחלץ פרמטרים מהנתיב של הבקשה

    path = event.get('path', '') or event.get('rawPath', '')
    return path.split('/')[-1] if path else None

def extract_request_body(event):

    # מחלץ ומפענח את גוף הבקשה

    import json
    
    body = event.get("body", "{}")
    if not body:
        return {}
    
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None

def get_client_ip(event):

    # מחזיר את כתובת ה-IP של הלקוח
    # שימושי לסטטיסטיקות ולוגים

    # ניסיון לקבל IP מכמה מקומות אפשריים
    source_ip = event.get('requestContext', {}).get('identity', {}).get('sourceIp')
    if source_ip:
        return source_ip
    
    # בדיקה בheaders עבור X-Forwarded-For
    headers = event.get('headers', {})
    forwarded_for = headers.get('X-Forwarded-For', headers.get('x-forwarded-for'))
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    
    return 'unknown'