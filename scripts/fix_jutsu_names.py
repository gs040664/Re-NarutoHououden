import json
import os
import re

db_path = r'c:\Users\Xin58696e\Desktop\NarutoHououden\database_json\db_jutsus.json'
chapters_dir = r'c:\Users\Xin58696e\Desktop\NarutoHououden\rewritten_chapters'

with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Rule: Category is "忍術" -> Add "忍法．" prefix
# Exceptions: "影分身", "多重影分身"
exceptions = ["影分身", "多重影分身"]

jutsu_data = []
for j in db:
    name = j['name'].strip()
    category = j['category'].strip()
    # Handle specific common names and variants
    jutsu_data.append({"name": name, "category": category})
    # Add variant without dots for matching
    base_name = name.split('．')[-1].split('·')[-1].split('·')[-1]
    if base_name != name:
        jutsu_data.append({"name": base_name, "category": category})

# Sort by name length descending to avoid partial matches
jutsu_data.sort(key=lambda x: len(x['name']), reverse=True)

patterns_to_fix = [
    (r'忍法·亂獅子之術', '忍法．亂獅子髮之術'),
    (r'亂獅子之術', '忍法．亂獅子髮之術'),
    (r'忍法·水遁', '水遁'),
    (r'忍法·火遁', '火遁'),
    (r'忍法·雷遁', '雷遁'),
    (r'忍法·土遁', '土遁'),
    (r'忍法·風遁', '風遁'),
    (r'忍法·通靈', '通靈'),
]

files = [f for f in os.listdir(chapters_dir) if f.endswith('.md')]

for filename in files:
    path = os.path.join(chapters_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Apply general patterns
    for old, new in patterns_to_fix:
        content = re.sub(old, new, content)
    
    # 2. Apply DB rules (Simplified approach for common jutsus)
    # Exceptions first: remove prefix if exists
    for ex in exceptions:
        content = content.replace(f"忍法．{ex}", ex)
        content = content.replace(f"忍法·{ex}", ex)
    
    # "忍術" category: add prefix
    # Need to be careful with overlaps. I'll focus on the ones I know I used.
    ninja_jutsus = ["亂獅子髮之術", "針地藏", "亂身衝", "蝦蟆口束縛術", "三日月之舞", "如雨露千本", "潛影蛇手", "牙通牙"]
    for nj in ninja_jutsus:
        # Avoid double prefix
        if f"忍法．{nj}" not in content:
            content = content.replace(nj, f"忍法．{nj}")
            # Also handle variant with half dot
            content = content.replace(f"忍法·{nj}", f"忍法．{nj}")

    # Standardize separator in all jutsus that have dots
    # Replace · with ． for consistent look if user prefers
    # content = content.replace('·', '．') # User specifically used ． in the rule
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Processed {len(files)} files.")
