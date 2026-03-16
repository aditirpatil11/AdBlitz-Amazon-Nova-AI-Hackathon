import json
import re


def parse_json_response(raw_text: str):
    cleaned = raw_text.strip()
    
    # Remove markdown fences
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    
    # Try parsing directly first
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    
    # Try fixing common issues: trailing commas
    fixed = re.sub(r',\s*}', '}', cleaned)
    fixed = re.sub(r',\s*]', ']', fixed)
    
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass
    
    # Try extracting JSON from surrounding text
    json_match = re.search(r'[\[{].*[\]}]', cleaned, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    raise json.JSONDecodeError(f"Could not parse JSON from response", cleaned, 0)