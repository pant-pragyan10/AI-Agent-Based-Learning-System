import json
import re


def clean_llm_json(response_text: str):
    """
    Extracts valid JSON from LLM response.
    Handles cases where model adds extra text.
    """

    try:
        return json.loads(response_text)
    except:
        pass

    # Try extracting JSON block using regex
    match = re.search(r"\{.*\}", response_text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return None