import re
from typing import Dict, Any, List

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.IGNORECASE)
IP_RE = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
URL_RE = re.compile(r"https?://\S+")

LEAK_KEYWORDS = [
    "leak",
    "leaked",
    "database",
    "data breach",
    "breach",
    "dump",
    "credentials",
    "passwords",
    "account dump",
    "combo list",
    "user data",
    "pastebin",
    "exposed",
    "hacked"
]

def find_emails(text: str):
    return EMAIL_RE.findall(text or "")


def find_ips(text: str):
    return IP_RE.findall(text or "")


def find_urls(text: str):
    return URL_RE.findall(text or "")


def contains_leak_keywords(text: str):
    text_l = (text or "").lower()
    matches = [kw for kw in LEAK_KEYWORDS if kw in text_l]
    return matches


def score_post(text: str):

    emails = find_emails(text)
    ips = find_ips(text)
    urls = find_urls(text)
    kws = contains_leak_keywords(text)

    score = 0
    flags = []

    score += len(kws) * 25
    score += len(emails) * 20
    score += len(ips) * 10
    score += len(urls) * 5

    if kws:
        flags.append("keywords")
    if emails:
        flags.append("emails")
    if ips:
        flags.append("ips")
    if urls:
        flags.append("urls")

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
        "emails": emails,
        "ips": ips,
        "urls": urls,
    }  