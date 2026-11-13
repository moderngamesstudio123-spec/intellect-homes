import os
import re

php_files = [f for f in os.listdir('.') if f.endswith('.php')] + [os.path.join('includes', f) for f in os.listdir('includes') if f.endswith('.php')]

for pf in php_files:
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    wp_matches = re.findall(r'https?://intellecthomes\.com\.au[^\s"\'<>]*', content)
    if wp_matches:
        print(f"File {pf} has {len(wp_matches)} intellecthomes links:")
        for m in wp_matches[:5]:
            print("  ", m)
    else:
        print(f"File {pf}: Clean! No external intellecthomes links.")
