def determine_request_method(event):
    """Determine the request method from Lambda Function URL event"""
    
    print(f"DEBUG: Full event structure: {event}")
    
    # Check requestContext.http.method (Lambda Function URL format)
    if 'requestContext' in event and 'http' in event['requestContext']:
        http_context = event['requestContext']['http']
        print(f"DEBUG: http_context: {http_context}")
        method = http_context.get('method')
        if method:
            print(f"DEBUG: Found method in requestContext.http: {method}")
            return method
    
    # Check top level httpMethod (API Gateway v1)
    if 'httpMethod' in event:
        method = event['httpMethod']
        print(f"DEBUG: Found httpMethod: {method}")
        return method
    
    # Check for body to infer POST
    body = event.get('body')
    if body:
        print(f"DEBUG: Found body, inferring POST: {body}")
        return 'POST'
    
    print("DEBUG: Defaulting to GET")
    return 'GET'

def extract_path_parameter(event):
    """Extract parameters from the request path"""
    path = event.get('path', '') or event.get('rawPath', '')
    return path.split('/')[-1] if path else None

def extract_request_body(event):
    """Extract and decode the request body"""
    import json
    
    body = event.get("body", "{}")
    if not body:
        return {}
    
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None

def get_client_ip(event):
    """Get the client's IP address"""
    # Try Lambda Function URL format first
    if 'requestContext' in event and 'http' in event['requestContext']:
        source_ip = event['requestContext']['http'].get('sourceIp')
        if source_ip:
            return source_ip
    
    return 'unknown'