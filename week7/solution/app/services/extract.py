import re
from typing import List, Dict

def extract_action_items(text: str) -> List[Dict[str, str]]:
    """
    Extracts action items from text using advanced pattern matching.
    Supports:
    - TODO: ...
    - FIXME: ...
    - BUG: ...
    - [!] High priority markers
    - [ ] Checkbox style
    """
    items = []
    
    # Pattern: Optional marker -> Keyword -> Colon -> Content
    pattern = r'(?:\[([!x ])\]\s*)?\b(TODO|FIXME|BUG)\b:?\s*(.+)'
    
    lines = text.split('\n')
    for line in lines:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            marker, keyword, content = match.groups()
            priority = "Normal"
            if marker == "!":
                priority = "High"
            elif keyword.upper() == "BUG":
                priority = "Critical"
                
            items.append({
                "type": keyword.upper(),
                "content": content.strip(),
                "priority": priority,
                "original_line": line.strip()
            })
            
    return items
