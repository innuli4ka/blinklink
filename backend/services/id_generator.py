import random
import string

def generate_short_id(length=6):
    # יוצר מזהה קצר אקראי עבור הקישור המקוצר
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_custom_id(custom_id):
    # בדיקת תקינות המזהה
    if not custom_id or len(custom_id) < 3:
        return None, "Custom ID must be at least 3 characters long"
    
    # בדיקה שהמזהה מכיל רק תווים מותרים
    allowed_chars = string.ascii_letters + string.digits + '-_'
    if not all(c in allowed_chars for c in custom_id):
        return None, "Custom ID can only contain letters, numbers, hyphens and underscores"
    
    return custom_id, None