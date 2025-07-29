import json
from services.database_service import save_short_url
from services.id_generator import generate_short_id, validate_url
from utils.response_builder import create_error_response, create_success_response

def handle_create_request(event):
    try:
        # Extract data from request body
        body = json.loads(event.get("body", "{}"))
        original_url = body.get("url")
        
        # Check if URL is not empty
        if not original_url:
            return create_error_response(400, "Missing URL parameter")
        
        # Validate URL format and safety
        is_valid, error_message = validate_url(original_url)
        if not is_valid:
            return create_error_response(400, error_message)
        
        # Generate new short ID
        short_id = generate_short_id()
        
        # Save URL to database
        success = save_short_url(short_id, original_url)
        
        if not success:
            return create_error_response(500, "Failed to save URL")
        
        # Return short ID to user
        return create_success_response({"short_id": short_id})
        
    except json.JSONDecodeError:
        return create_error_response(400, "Invalid JSON format")
    except Exception as e:
        print(f"Error in handle_create_request: {str(e)}")
        return create_error_response(500, "Failed to create short URL")