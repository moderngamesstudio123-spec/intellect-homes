import os
import re

missing = []
total_checked = 0

all_php_files = []
for root, dirs, files in os.walk('.'):
    if 'raw_pages' in root:
        continue
    for f in files:
        if f.endswith('.php'):
            all_php_files.append(os.path.join(root, f))

for pf in all_php_files:
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find all assets/images/xxx or ../assets/images/xxx
    imgs = re.findall(r'(?:\.\./)?assets/images/([a-zA-Z0-9_\-\.]+)', content)
    for img in imgs:
        total_checked += 1
        path = os.path.join('assets', 'images', img)
        if not os.path.exists(path):
            missing.append((pf, img))

print(f"Total asset references checked: {total_checked}")
if missing:
    print(f"Missing assets ({len(missing)}):")
    for m in set(missing):
        print(" ", m)
else:
    print("All referenced assets exist locally on disk! 100% verified.")
