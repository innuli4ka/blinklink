import json
from services.database_service import save_short_url
from services.id_generator import generate_short_id
from utils.response_builder import create_error_response, create_success_response

def handle_create_request(event):

    # מטפל בבקשות POST - יצירת קישור מקוצר חדש
    # מקבל קישור ארוך ויוצר עבורו מזהה קצר

    try:
        # חילוץ הנתונים מגוף הבקשה
        body = json.loads(event.get("body", "{}"))
        original_url = body.get("url")
        
        # בדיקה שהקישור לא ריק
        if not original_url:
            return create_error_response(400, "Missing URL parameter")
        
        # יצירת מזהה קצר חדש
        short_id = generate_short_id()
        print(f"Creating short URL: {short_id} -> {original_url}")
        
        # שמירת הקישור במסד הנתונים
        success = save_short_url(short_id, original_url)
        
        if not success:
            return create_error_response(500, "Failed to save URL")
        
        # החזרת המזהה הקצר למשתמש
        return create_success_response({"short_id": short_id})
        
    except json.JSONDecodeError:
        return create_error_response(400, "Invalid JSON format")
    except Exception as e:
        print(f"Error creating short URL: {str(e)}")
        return create_error_response(500, "Failed to create short URL")