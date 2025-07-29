import random
import string
from services.database_service import url_exists

def generate_short_id(length=6, max_attempts=10):
    """
    Generate a unique short ID, checking for collisions
    """
    characters = string.ascii_letters + string.digits
    
    for attempt in range(max_attempts):
        short_id = ''.join(random.choices(characters, k=length))
        
        # Check if this ID already exists
        if not url_exists(short_id):
            return short_id
    
    # If we couldn't find a unique ID after max_attempts, try with longer length
    return generate_short_id(length + 1, max_attempts)

def validate_url(url):
    """
    Validate that the URL is safe and properly formatted
    """
    import re
    from urllib.parse import urlparse
    
    if not url or len(url) > 2048:  # Reasonable URL length limit
        return False, "URL is empty or too long"
    
    # Basic URL format validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False, "Invalid URL format"
    
    # Parse URL to check components
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return False, "Only HTTP and HTTPS URLs are allowed"
        
        # Block potentially dangerous domains/IPs
        dangerous_patterns = [
            'localhost', '127.0.0.1', '0.0.0.0', '10.', '192.168.', '172.'
        ]
        
        if any(pattern in parsed.netloc.lower() for pattern in dangerous_patterns):
            return False, "Internal/private URLs are not allowed"
            
    except Exception:
        return False, "Failed to parse URL"
    
    return True, None