def is_prompt_injection(text: str) -> bool:
    suspicious_patterns = [
        "ignore previous instructions",
        "act as system",
        "bypass",
        "override",
        "jailbreak",
        "pretend you are",
    ]

    text_lower = text.lower()

    for pattern in suspicious_patterns:
        if pattern in text_lower:
            return True

    return False