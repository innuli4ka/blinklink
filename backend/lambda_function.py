import json
from handlers.redirect_handler import handle_redirect_request
from handlers.create_handler import handle_create_request
from utils.response_builder import create_error_response
from utils.request_parser import determine_request_method

def lambda_handler(event, context):
   
# הפונקציה הראשית שמטפלת בכל הבקשות
# מפנה לטיפול המתאים בהתאם לסוג הבקשה
    
    try:
        # הדפסת מידע על הבקשה לצורכי ניפוי שגיאות
        print("Received request:", json.dumps(event, indent=2))
        
        # קביעת סוג הבקשה
        request_method = determine_request_method(event)
        print(f"Request method: {request_method}")
        
        # ניתוב הבקשה לטיפול המתאים
        if request_method == 'GET':
            return handle_redirect_request(event)
        elif request_method == 'POST':
            return handle_create_request(event)
        else:
            return create_error_response(405, "Method not allowed")
    
    except Exception as e:
        # טיפול בשגיאות כלליות לא צפויות
        print(f"Unexpected error in lambda_handler: {str(e)}")
        return create_error_response(500, "Internal server error")