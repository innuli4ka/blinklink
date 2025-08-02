import json
import time
import logging
from datetime import datetime
from handlers.redirect_handler import handle_redirect_request
from handlers.create_handler import handle_create_request
from utils.response_builder import create_error_response
from utils.request_parser import determine_request_method

# Configure logging for CloudWatch metrics
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Start timing for end-to-end latency metric
    start_time = time.time()
    request_id = context.aws_request_id
    
    try:
        # Determine request method
        request_method = determine_request_method(event)
        
        # Handle different request types
        if request_method == 'POST':
            # Handle URL shortening
            response = handle_create_request(event)
            
            # Log URL shortened metric if successful
            if response.get('statusCode') == 200:
                # Parse response to get short_id
                body = json.loads(response.get('body', '{}'))
                short_id = body.get('short_id', 'unknown')
                
                # 1. Log URL shortened for business metric
                logger.info(f"{datetime.utcnow().isoformat()} {request_id} URL_SHORTENED short_id={short_id}")
            
        elif request_method == 'GET':
            # Handle redirect
            response = handle_redirect_request(event)
            
            # Extract short_id from path for logging
            path = event.get('path', '') or event.get('rawPath', '')
            short_id = path.strip('/')
            
            # Log redirect metrics
            if response.get('statusCode') == 302:
                # 2. Log successful redirect for business metric
                logger.info(f"{datetime.utcnow().isoformat()} {request_id} REDIRECT_SUCCESS short_id={short_id}")
            else:
                # 2. Log failed redirect for business metric
                logger.info(f"{datetime.utcnow().isoformat()} {request_id} REDIRECT_FAILED short_id={short_id}")
                
        elif request_method == 'OPTIONS':
            # Handle CORS preflight
            response = {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Max-Age": "86400"
                },
                'body': ''
            }
        else:
            response = create_error_response(405, "Method not allowed")
        
        # Calculate end-to-end latency
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)
        
        # 6. Log request latency for performance metric
        logger.info(f"{datetime.utcnow().isoformat()} {request_id} REQUEST_LATENCY {latency_ms}")
        
        return response
        
    except Exception as e:
        # Log errors
        logger.error(f"{datetime.utcnow().isoformat()} {request_id} ERROR {str(e)}")
        
        # Calculate latency even for errors
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)
        logger.info(f"{datetime.utcnow().isoformat()} {request_id} REQUEST_LATENCY {latency_ms}")
        
        return create_error_response(500, "Internal server error")