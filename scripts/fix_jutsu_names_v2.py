import json
import os
import re

chapters_dir = r'c:\Users\Xin58696e\Desktop\NarutoHououden\rewritten_chapters'

# DOT regex that matches various dot-like characters
DOT = r'[·．·.]'

# Mapping of (regex_pattern, replacement)
# We use DOT in patterns to handle inconsistent input
FIXES = [
    (rf'忍法{DOT}亂獅子之術', '忍法．亂獅子髮之術'),
    (rf'亂獅子之術', '忍法．亂獅子髮之術'),
    (rf'忍法{DOT}亂獅子髮之術', '忍法．亂獅子髮之術'),
    
    # Category based fixes: remove "忍法．" for non-ninja-jutsu categories
    (rf'忍法{DOT}水遁', '水遁'),
    (rf'忍法{DOT}火遁', '火遁'),
    (rf'忍法{DOT}雷遁', '雷遁'),
    (rf'忍法{DOT}土遁', '土遁'),
    (rf'忍法{DOT}風遁', '風遁'),
    (rf'忍法{DOT}通靈', '通靈'),
    
    # Exceptions: 影分身, 多重影分身 (Remove "忍法．" prefix)
    (rf'忍法{DOT}多重影分身', '多重影分身'),
    (rf'忍法{DOT}影分身', '影分身'),
]

files = [f for f in os.listdir(chapters_dir) if f.endswith('.md')]

for filename in files:
    path = os.path.join(chapters_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for pattern, replacement in FIXES:
        new_content = re.sub(pattern, replacement, new_content)
    
    # Also handle some specific ninja jutsus that SHOULD have "忍法．"
    ninja_jutsus = ["針地藏", "亂身衝", "蝦蟆口束縛術", "三日月之舞"]
    for nj in ninja_jutsus:
        # If the jutsu is present but lacks "忍法．" and is not already prefixed by some DOT
        # This is a bit complex for regex, so simple replace with check
        if nj in new_content:
            # Check if it's already prefixed
            if not re.search(rf'忍法{DOT}{nj}', new_content):
                new_content = new_content.replace(nj, f"忍法．{nj}")
            else:
                # Standardize DOT if it was prefixed with wrong dot
                new_content = re.sub(rf'忍法{DOT}{nj}', f"忍法．{nj}", new_content)

    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")

print("Done.")
