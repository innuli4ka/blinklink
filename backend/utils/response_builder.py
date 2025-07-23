import json

def create_error_response(status_code, error_message):

    # יוצר תגובת שגיאה סטנדרטית

    return {
        'statusCode': status_code,
        'headers': {"Content-Type": "application/json"},
        'body': json.dumps({"error": error_message})
    }

def create_success_response(data):

    # יוצר תגובת הצלחה עם נתונים

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json"},
        'body': json.dumps(data)
    }

def create_redirect_response(url):

    # יוצר תגובת הפניה לקישור המקורי

    return {
        'statusCode': 302,
        'headers': {
            'Location': url,
            'Content-Type': 'text/html'
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