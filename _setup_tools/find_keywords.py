import os
import re

for root, dirs, files in os.walk('.'):
    if 'raw_pages' in root or '_setup_tools' in root:
        continue
    for f in files:
        if f.endswith('.php'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            # Find any mention of 2026 or Guide or Inclusion or Request
            matches = re.findall(r'.{0,50}(?:2026|Guide|Inclusion|Request).{0,50}', content, re.IGNORECASE)
            # filter out image names with 2026
            real_matches = [m.strip() for m in matches if not 'assets/images' in m and not 'WhatsApp' in m]
            if real_matches:
                print(f"=== {path} ===")
                for rm in set(real_matches):
                    print("  ", rm)

