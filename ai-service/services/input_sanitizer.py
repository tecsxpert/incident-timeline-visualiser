import re

INJECTION_PATTERN = re.compile(
    r"ignore previous instructions|disregard|you are now|act as|jailbreak|system prompt|<script|drop table|union select",
    re.IGNORECASE
)


def sanitize(value: str, field: str):
    """Returns (cleaned_value, error_or_None)"""
    if not isinstance(value, str):
        return "", f"'{field}' must be a string."

    # Remove HTML tags and null bytes
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("\x00", "").strip()

    if len(value) > 2000:
        return "", f"'{field}' is too long (max 2000 characters)."

    if INJECTION_PATTERN.search(value):
        return "", f"'{field}' contains disallowed content."

    return value, None


def sanitize_fields(data: dict, fields: list):
    """Sanitize multiple fields. Returns (cleaned_data, error_or_None)"""
    cleaned = dict(data)
    for field in fields:
        if field not in cleaned or cleaned[field] is None:
            continue
        cleaned[field], err = sanitize(str(cleaned[field]), field)
        if err:
            return {}, err
    return cleaned, None