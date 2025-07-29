
import json

def _get_cors_headers():
    """Return consistent CORS headers for all responses"""
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Max-Age": "86400"
    }

def create_error_response(status_code, error_message):
    """Create standardized error response"""
    return {
        'statusCode': status_code,
        'headers': _get_cors_headers(),
        'body': json.dumps({"error": error_message})
    }

def create_success_response(data):
    """Create success response with data"""
    return {
        'statusCode': 200,
        'headers': _get_cors_headers(),
        'body': json.dumps(data)
    }

def create_redirect_response(url):
    """Create redirect response - should use same CORS headers for consistency"""
    return {
        'statusCode': 302,
        'headers': {
            'Location': url,
            'Content-Type': 'text/html',
            # Use the same CORS headers as other responses
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
        },
        'body': _create_redirect_html(url)
    }

def _create_redirect_html(url):
    """Create HTML redirect page"""
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