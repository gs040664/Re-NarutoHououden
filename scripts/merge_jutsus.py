import json
import re
import os

db_path = r'c:\Users\Xin58696e\Desktop\NarutoHououden\database_json\db_jutsus.json'
wiki2_path = r'c:\Users\Xin58696e\Desktop\NarutoHououden\data\jutsu2_wiki.txt'
wiki3_path = r'c:\Users\Xin58696e\Desktop\NarutoHououden\data\jutsu3_wiki.txt'

def normalize(name):
    """Normalize names for matching."""
    if not name: return ""
    # Normalize dots and spaces
    name = name.replace('‧', '．').replace('·', '．').replace('.', '．').strip()
    # Remove common category prefixes often found in wiki3
    prefixes = ["忍術 ", "體術 ", "幻術 ", "祕傳 ", "秘術 ", "封印術 ", "時空間忍術 ", "傀儡術 ", "醫療術．", "醫療術 ", "血繼限界 ", "禁術 "]
    for p in prefixes:
        if name.startswith(p):
            name = name[len(p):].strip()
    return name

# Load existing DB
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Use original data as base, but we will re-index at the end.
# Group by normalized name
jutsu_map = {}
for j in db:
    norm = normalize(j['name'])
    if norm not in jutsu_map:
        jutsu_map[norm] = j

# Parse Wiki 2 (Descriptions)
with open(wiki2_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_category = ""
current_jutsu = None
for line in lines:
    line = line.replace('\n', '')
    if not line.strip(): continue
    if not line.startswith(' '):
        current_category = line.strip()
        continue
    if line.startswith('    ') and not line.strip().startswith(' '):
        raw_name = line.strip()
        # Handle "Name (Alt)"
        clean_name = re.sub(r'[（\(].*?[）\)]', '', raw_name).strip()
        norm = normalize(clean_name)
        
        if norm not in jutsu_map:
            new_jutsu = {
                "id": "",
                "category": current_category,
                "name": raw_name,
                "rank": "",
                "description": "",
                "seals": "",
                "users": ""
            }
            db.append(new_jutsu)
            jutsu_map[norm] = new_jutsu
        
        current_jutsu = jutsu_map[norm]
        # Update category if missing or generic
        if not current_jutsu.get('category') or current_jutsu['category'] == "未分類":
            current_jutsu['category'] = current_category
        continue
    
    if current_jutsu and line.strip():
        # Append description only if it's longer than current
        if len(line.strip()) > 5:
            if not current_jutsu['description'] or len(current_jutsu['description']) < len(line.strip()):
                if current_jutsu['description']:
                    current_jutsu['description'] += " " + line.strip()
                else:
                    current_jutsu['description'] = line.strip()

# Parse Wiki 3 (Ranks)
with open(wiki3_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_rank = ""
for line in lines:
    line = line.replace('\n', '')
    if not line.strip(): continue
    if "級術" in line and not line.startswith(' '):
        current_rank = line.replace('級術', '').strip()
        continue
    if line.startswith('    '):
        content = line.strip()
        # Pattern: [Type] [Name]-[User]
        # Allow optional hyphen for user
        parts = content.split('-', 1)
        name_part = parts[0].strip()
        user_part = parts[1].strip() if len(parts) > 1 else ""
        
        norm = normalize(name_part)
        
        if norm in jutsu_map:
            target = jutsu_map[norm]
            if not target.get('rank'): target['rank'] = current_rank
            if not target.get('users') and user_part: target['users'] = user_part
        else:
            # Create new entry
            # Extract actual name from "Type Name"
            actual_name = normalize(name_part)
            new_jutsu = {
                "id": "",
                "category": "其他", # Temp
                "name": name_part,
                "rank": current_rank,
                "description": "",
                "seals": "",
                "users": user_part
            }
            db.append(new_jutsu)
            jutsu_map[norm] = new_jutsu

# Final cleanup and re-indexing
final_db = []
seen = set()
for j in db:
    norm = normalize(j['name'])
    if norm not in seen:
        final_db.append(j)
        seen.add(norm)

# Re-index
for i, jutsu in enumerate(final_db):
    jutsu['id'] = f"jutsu_{i+1:04d}"

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(final_db, f, ensure_ascii=False, indent=2)

print(f"Final merge complete. Total unique jutsus: {len(final_db)}")
