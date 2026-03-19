import urllib.request
import urllib.parse
import json
import sys
import os

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_batch.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    converted = convert_file(input_file)
    if converted:
        if len(sys.argv) >= 3:
            output_file = sys.argv[2]
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted)
            print(f"Converted and saved to {output_file}")
        else:
            print(converted)
