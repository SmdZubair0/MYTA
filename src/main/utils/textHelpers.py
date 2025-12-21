import re
import json
from typing import Optional

def extract_json(text: str) -> dict:
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in LLM response")

    json_str = match.group(0)
    return json.loads(json_str)

def normalize_text(value: Optional[str]) -> str:
    return value.lower().strip() if value else ""