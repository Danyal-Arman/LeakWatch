import re
from typing import Dict, Any, List

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}")
IP_RE = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
URL_RE = re.compile(r"https?://\S+")

LEAK_KEYWORDS = [
    "leak",
    "leaked",
    "database",
    "dump",
    "credentials",
    "passwords",
    "combo",
    "pastebin",
    "dumps",
    "credit card",
    "ssn",
    "credentials",
]

def find_emails(text: str) -> List[str]:
    return EMAIL_RE.findall(text or "")


def find_ips(text: str) -> List[str]:
    return IP_RE.findall(text or "")


def find_urls(text: str) -> List[str]:
    return URL_RE.findall(text or "")


def contains_leak_keywords(text: str) -> List[str]:
    text_l = (text or "").lower()
    matches = [kw for kw in LEAK_KEYWORDS if kw in text_l]
    return matches


def score_post(text: str) -> Dict[str, Any]:
    """Return dict with flags, score (0-100), and severity."""
    emails = find_emails(text)
    ips = find_ips(text)
    urls = find_urls(text)
    kws = contains_leak_keywords(text)

    score = 0
    flags: List[str] = []

    if kws:
        score += 70
        flags.append("keywords: " + ",".join(kws))
    if emails:
        score += 40
        flags.append("emails")
    if ips:
        score += 15
        flags.append("ips")
    if urls:
        score += 10
        flags.append("urls")

    # clamp
    if score > 100:
        score = 100

    if score >= 40:
        severity = "high"
    elif score >= 30:
        severity = "medium"
    else:
        severity = "low"

    return {
        "score": score,
        "severity": severity,
        "flags": flags,
        "emails": emails,
        "ips": ips,
        "urls": urls,
    } 