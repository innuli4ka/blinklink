import json
from handlers.redirect_handler import handle_redirect_request
from handlers.create_handler import handle_create_request
from utils.response_builder import create_error_response
from utils.request_parser import determine_request_method

def lambda_handler(event, context):
    try:
        # Debug: Return the event structure and method detection
        request_method = determine_request_method(event)
        
        debug_info = {
            "detected_method": request_method,
            "event_keys": list(event.keys()),
            "has_body": bool(event.get('body')),
            "body_content": event.get('body', 'NO BODY'),
            "path": event.get('path', 'NO PATH'),
            "rawPath": event.get('rawPath', 'NO RAW PATH')
        }
        
        # For now, return debug info instead of processing
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Content-Type": "application/json"
            },
            'body': json.dumps(debug_info)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            'body': json.dumps({"error": str(e)})
        }