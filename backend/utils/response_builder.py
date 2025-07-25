import json

def _get_cors_headers():
    """מחזיר headers של CORS"""
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
    }

def create_error_response(status_code, error_message):

    # יוצר תגובת שגיאה סטנדרטית

    return {
        'statusCode': status_code,
        'headers': _get_cors_headers(),
        'body': json.dumps({"error": error_message})
    }

def create_success_response(data):

    # יוצר תגובת הצלחה עם נתונים

    return {
        'statusCode': 200,
        'headers': _get_cors_headers(),
        'body': json.dumps(data)
    }

def create_redirect_response(url):

    # יוצר תגובת הפניה לקישור המקורי

    return {
        'statusCode': 302,
        'headers': {
            'Location': url,
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Headers': "Content-Type",
            'Access-Control-Allow-Methods': "GET, POST, OPTIONS"
        },
        'body': _create_redirect_html(url)
    }

def _create_redirect_html(url):

    # יוצר עמוד HTML להפניה אוטומטית
    # כולל גם הפניה דרך JavaScript למקרים שההפניה הרגילה לא עובדת

    return f'''
    <html>
        <head>
            <meta http-equiv="refresh" content="0;url={url}">
            <title>Redirecting...</title>
        </head>
        <body>
            <p>Redirecting to <a href="{url}">{url}</a></p>
            <script>window.location.href = "{url}";</script>
        </body>
    </html>
    '''