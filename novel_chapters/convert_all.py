import urllib.request
import urllib.parse
import json
import sys
import os
import time

def convert_file(file_path, converter='Taiwan'):
    url = "https://api.zhconvert.org/convert"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    payload = {
        'text': text,
        'converter': converter,
        'modules': json.dumps({"Naruto": 1, "Typo": 1})
    }
    
    data = urllib.parse.urlencode(payload).encode('utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('code') == 0:
                return result['data']['text']
            else:
                print(f"API Error: {result.get('msg')}", file=sys.stderr)
                return None
    except Exception as e:
        print(f"Request Error: {e}", file=sys.stderr)
        return None

def main():
    base_dir = r"c:\Users\gs040664\Desktop\NarutoHououden\novel_chapters"
    original_dir = os.path.join(base_dir, "original")
    taiwanized_dir = os.path.join(base_dir, "taiwanized")
    
    if not os.path.exists(original_dir):
        print(f"Error: {original_dir} does not exist.")
        return
    if not os.path.exists(taiwanized_dir):
        os.makedirs(taiwanized_dir)
        
    files = sorted(os.listdir(original_dir))
    count = 0
    total = len([f for f in files if f.endswith(".txt")])
    
    for filename in files:
        if not filename.endswith(".txt"):
            continue
            
        # Extract prefix (e.g., '005')
        prefix = filename.split('_')[0]
        if not prefix.isdigit():
            # For special files like '001_讀者...' we still use the prefix
            pass
            
        output_filename = f"{prefix}_Taiwan.txt"
        output_path = os.path.join(taiwanized_dir, output_filename)
        
        if os.path.exists(output_path):
            # print(f"Skipping {filename}, already exists as {output_filename}")
            continue
            
        count += 1
        print(f"[{count}/{total}] Converting {filename} -> {output_filename}...")
        input_path = os.path.join(original_dir, filename)
        converted = convert_file(input_path)
        
        if converted:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(converted)
            print(f"Successfully converted {filename}")
            # Sleep slightly to be polite to the API
            time.sleep(1)
        else:
            print(f"Failed to convert {filename}")

if __name__ == "__main__":
    main()
