from groq import Groq
import json
import os
import re

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ai_detect(password):

    prompt = f"""
You are a cybersecurity expert.

Analyze the following PASSWORD and determine whether it is weak or strong.

Consider:
- Common passwords
- Easy to guess passwords
- Dictionary words
- Short length
- Missing uppercase letters
- Missing lowercase letters
- Missing numbers
- Missing special characters

Return ONLY valid JSON.

Format:

{{
    "isWeak": true,
    "severity": "high",
    "confidence": 95,
    "reason": "Short explanation",
    "recommendation": "Short recommendation"
}}

Allowed severity values:
- high
- medium
- low

Password:
{password}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    print("GROQ RESPONSE:")
    print(content)

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:
        return json.loads(match.group())

    return {
        "isWeak": False,
        "severity": "low",
        "confidence": 0,
        "reason": "Failed to parse AI response"
    }