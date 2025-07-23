import random
import string
from .database_service import url_exists

def generate_short_id(length=6, max_attempts=10):

    # יוצר מזהה קצר אקראי עבור הקישור המקוצר
    # משתמש באותיות ומספרים באורך של 6 תווים כברירת מחדל
    # בודק שהמזהה לא קיים כבר במסד הנתונים

    characters = string.ascii_letters + string.digits
    
    for attempt in range(max_attempts):
        short_id = ''.join(random.choices(characters, k=length))
        
        # בדיקה שהמזהה לא קיים כבר
        if not url_exists(short_id):
            return short_id
        
        print(f"ID collision detected for {short_id}, trying again (attempt {attempt + 1})")
    
    # אם לא הצלחנו למצוא מזהה ייחודי, נגדיל את האורך
    print(f"Could not generate unique ID in {max_attempts} attempts, increasing length")
    return generate_short_id(length + 1, max_attempts)

def generate_custom_id(custom_id):

    # מאפשר למשתמש להגדיר מזהה מותאם אישית
    # בודק שהמזהה לא קיים כבר ושהוא תקין

    # בדיקת תקינות המזהה
    if not custom_id or len(custom_id) < 3:
        return None, "Custom ID must be at least 3 characters long"
    
    # בדיקה שהמזהה מכיל רק תווים מותרים
    allowed_chars = string.ascii_letters + string.digits + '-_'
    if not all(c in allowed_chars for c in custom_id):
        return None, "Custom ID can only contain letters, numbers, hyphens and underscores"
    
    # בדיקה שהמזהה לא קיים כבר
    if url_exists(custom_id):
        return None, "Custom ID already exists"
    
    return custom_id, None