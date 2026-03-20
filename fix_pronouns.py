import re
import os
import sys

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Heuristic: Replace "我" in narrative (outside of 「」 and 『』 and "")
    # This is a bit complex for regex. A simpler way is to split by quotes.
    
    # regex for quotes: 「...」 or 『...』
    parts = re.split(r'(「[^」]*」|『[^』]*』)', content)
    
    new_parts = []
    for part in parts:
        if part.startswith('「') or part.startswith('『'):
            # Inside dialogue or inner thought quotes, keep it
            new_parts.append(part)
        else:
            # Narrative, replace "我" with "悠羽" or "她"
            # We use "悠羽" for the first match or subject, "她" for subsequent?
            # For simplicity, let's use "悠羽" mostly or contextually.
            # Here I'll just use a simple list of common patterns to replace.
            
            # Basic replacements
            part = part.replace('我的', '悠羽的')
            part = part.replace('我們', '悠羽一行人')
            part = part.replace('我，', '悠羽，')
            part = part.replace('我。', '悠羽。')
            part = part.replace('我 ', '悠羽 ')
            
            # More general "我" -> "悠羽" if it's the subject/object in narrative
            # But be careful not to break words. In Chinese, "我" is a single character.
            part = part.replace('我', '悠羽')
            
            new_parts.append(part)
            
    new_content = ''.join(new_parts)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            if os.path.exists(path):
                fix_file(path)
                print(f"Fixed {path}")
            else:
                print(f"File not found: {path}")
