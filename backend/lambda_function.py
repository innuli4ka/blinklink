import json
from handlers.redirect_handler import handle_redirect_request
from handlers.create_handler import handle_create_request
from utils.response_builder import create_error_response
from utils.request_parser import determine_request_method

def lambda_handler(event, context):
    try:
        # Add logging for debugging
        print(f"Event received: {json.dumps(event)}")
        
        # Determine request method
        request_method = determine_request_method(event)
        print(f"Request method: {request_method}")
        
        # Handle OPTIONS requests (CORS preflight)
        if request_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Max-Age": "86400",
                    "Content-Type": "application/json"
                },
                'body': json.dumps({"message": "CORS preflight successful"})
            }
        
        # Route the request to appropriate handler
        if request_method == 'GET':
            # Check if this is a redirect request (has path parameter)
            path = event.get('path', '') or event.get('rawPath', '')
            if path and path != '/' and not path.endswith('/'):
                return handle_redirect_request(event)
            else:
                return create_error_response(404, "Invalid request")
                
        elif request_method == 'POST':
            return handle_create_request(event)
        else:
            return create_error_response(405, "Method not allowed")
    
    except Exception as e:
        print(f"Lambda error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return create_error_response(500, "Internal server error")