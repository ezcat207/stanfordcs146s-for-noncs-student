from __future__ import annotations

import json
from typing import List

try:
    from ollama import chat
    from pydantic import BaseModel
except ImportError:
    # Just in case dependencies are missing, though the user should have them
    pass

class ActionItems(BaseModel):
    items: List[str]

def extract_action_items_llm(text: str, model_name: str = "deepseek-v3.1:671b-cloud") -> List[str]:
    """
    Extracts action items from text using an LLM via Ollama.
    """
    print(f"Extracting with {model_name}...")
    
    prompt = f"""
    Extract all action items (tasks, todos) from the following text.
    Return ONLY a JSON object with a key 'items' containing a list of strings.
    Do not include any other text.
    
    Text:
    {text}
    """

    try:
        response = chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            format=ActionItems.model_json_schema(), # Structured output
        )
        
        content = response['message']['content']
        data = ActionItems.model_validate_json(content)
        return data.items
        
    except Exception as e:
        print(f"Error extracting action items: {e}")
        return []

def extract_action_items(text: str) -> List[str]:
    """
    Legacy wrapper for the new LLM-based extraction.
    This ensures existing code calling 'extract_action_items' still works.
    """
    return extract_action_items_llm(text)
