import re

COMMON_PASSWORDS = {
    "123456",
    "12345678",
    "password",
    "password123",
    "admin",
    "admin123",
    "qwerty",
    "welcome",
    "abc123",
    "111111",
    "000000",
    "letmein",
    "test",
    "testing"
}


def analyze_password(password: str):
    score = 0
    flags = []

    # Common password
    if password.lower() in COMMON_PASSWORDS:
        score += 40
        flags.append("Common Password")

    # Length
    if len(password) < 8:
        score += 20
        flags.append("Less than 8 characters")

    # No uppercase
    if not re.search(r"[A-Z]", password):
        score += 15
        flags.append("No uppercase letter")

    # No lowercase
    if not re.search(r"[a-z]", password):
        score += 15
        flags.append("No lowercase letter")

    # No number
    if not re.search(r"\d", password):
        score += 10
        flags.append("No numeric digit")

    # No special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\]]", password):
        score += 10
        flags.append("No special character")

    score = min(score, 100)

    if score >= 70:
        severity = "high"
    elif score >= 40:
        severity = "medium"
    else:
        severity = "low"

    return {
        "score": score,
        "severity": severity,
        "flags": flags,
    }

COMMON_PASSWORDS = {
    "123456",
    "12345678",
    "password",
    "password123",
    "admin",
    "admin123",
    "qwerty",
    "welcome",
    "abc123",
    "111111",
    "000000",
    "letmein",
    "test",
    "testing"
}


def analyze_password(password: str):
    score = 0
    flags = []

    # Common password
    if password.lower() in COMMON_PASSWORDS:
        score += 40
        flags.append("Common Password")

    # Length
    if len(password) < 8:
        score += 20
        flags.append("Less than 8 characters")

    # No uppercase
    if not re.search(r"[A-Z]", password):
        score += 15
        flags.append("No uppercase letter")

    # No lowercase
    if not re.search(r"[a-z]", password):
        score += 15
        flags.append("No lowercase letter")

    # No number
    if not re.search(r"\d", password):
        score += 10
        flags.append("No numeric digit")

    # No special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\]]", password):
        score += 10
        flags.append("No special character")

    score = min(score, 100)

    if score >= 70:
        severity = "high"
    elif score >= 40:
        severity = "medium"
    else:
        severity = "low"

    return {
        "score": score,
        "severity": severity,
        "flags": flags,
    }