import json
from handlers.redirect_handler import handle_redirect_request
from handlers.create_handler import handle_create_request
from utils.response_builder import create_error_response
from utils.request_parser import determine_request_method

def lambda_handler(event, context):
    try:
        # קביעת סוג הבקשה
        request_method = determine_request_method(event)
        
        # טיפול ב-OPTIONS requests (CORS preflight)
        if request_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
                },
                'body': ''
            }
        
        # ניתוב הבקשה לטיפול המתאים
        if request_method == 'GET':
            return handle_redirect_request(event)
        elif request_method == 'POST':
            return handle_create_request(event)
        else:
            return create_error_response(405, "Method not allowed")
    
    except Exception as e:
        return create_error_response(500, "Internal server error")