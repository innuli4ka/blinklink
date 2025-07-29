from services.database_service import get_original_url
from utils.response_builder import create_error_response, create_redirect_response

def handle_redirect_request(event):
    # Extract path from request
    path = event.get('path', '') or event.get('rawPath', '')
    
    # Clean the path and extract short_id
    clean_path = path.strip('/')
    
    # Get the short_id - it should be the entire clean path for direct access
    short_id = clean_path
    
    print(f"Redirect request - Path: '{path}', Clean path: '{clean_path}', Short ID: '{short_id}'")
    
    # Check if short_id is valid and not empty
    if not short_id:
        return create_error_response(404, "Short URL not found")
    
    # Search for original URL in database
    try:
        original_url = get_original_url(short_id)
        
        if not original_url:
            return create_error_response(404, "Short URL not found")
        
        print(f"Redirecting {short_id} to {original_url}")
        return create_redirect_response(original_url)
        
    except Exception as e:
        print(f"Database error in redirect: {str(e)}")
        return create_error_response(500, "Database error occurred")