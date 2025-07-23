from services.database_service import get_original_url
from utils.response_builder import create_error_response, create_redirect_response

def handle_redirect_request(event):

    # מטפל בבקשות GET - הפניה מקישור מקוצר לקישור המקורי
    # מחלץ את המזהה הקצר מהנתיב ומחפש את הקישור המקורי במסד הנתונים

    # חילוץ הנתיב מהבקשה
    path = event.get('path', '') or event.get('rawPath', '')
    print(f"Processing redirect request for path: {path}")
    
    # קבלת המזהה הקצר מהחלק האחרון של הנתיב
    short_id = path.split('/')[-1]
    
    # בדיקה שהמזהה תקין ולא ריק
    if not short_id or short_id == 'shorten':
        return create_error_response(404, "Short URL not found")
    
    print(f"Looking up short ID: {short_id}")
    
    # חיפוש הקישור המקורי במסד הנתונים
    try:
        original_url = get_original_url(short_id)
        
        if not original_url:
            return create_error_response(404, "Short URL not found")
        
        print(f"Redirecting to: {original_url}")
        return create_redirect_response(original_url)
        
    except Exception as e:
        print(f"Database error during redirect: {str(e)}")
        return create_error_response(500, "Database error occurred")