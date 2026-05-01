import re

def sanitize_input(text: str) -> str:
    # Handle None or non-string types
    if text is None or not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove script-related keywords
    text = re.sub(r'(script|alert|onerror)', '', text, flags=re.IGNORECASE)

    # Remove special characters (optional but better)
    text = re.sub(r'[^\w\s]', '', text)

    # Remove extra spaces
    text = text.strip()

    return text