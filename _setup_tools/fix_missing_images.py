import os
import re
import urllib.request
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0'}

all_php_files = []
for root, dirs, files in os.walk('.'):
    if 'raw_pages' in root:
        continue
    for f in files:
        if f.endswith('.php'):
            all_php_files.append(os.path.join(root, f))

# First, let's remove srcset attributes from all PHP files because in pure PHP/HTML they just reference WordPress generated thumbnails
for pf in all_php_files:
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove srcset="..." and sizes="..."
    content = re.sub(r'\s+srcset=["\'][^"\']+["\']', '', content)
    content = re.sub(r'\s+sizes=["\'][^"\']+["\']', '', content)
    with open(pf, 'w', encoding='utf-8') as f:
        f.write(content)

print("Removed WordPress srcset and sizes attributes from all PHP files.")

# Now check which actual src="..." images are missing
missing_srcs = set()
for pf in all_php_files:
    with open(pf, 'r', encoding='utf-8') as f:
        content = f.read()
    srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    for s in srcs:
        fname = os.path.basename(s)
        local_path = os.path.join('assets', 'images', fname)
        if not os.path.exists(local_path):
            missing_srcs.add(fname)

print("Actual missing img src:", len(missing_srcs), missing_srcs)

# Try downloading any missing img src from intellecthomes
for fname in missing_srcs:
    downloaded = False
    for folder in ['2026/09', '2026/08', '2026/07', '2026/06']:
        url = f'https://intellecthomes.com.au/wp-content/uploads/{folder}/{fname}'
        dest = os.path.join('assets', 'images', fname)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                with open(dest, 'wb') as out:
                    out.write(resp.read())
            print(f"Successfully downloaded {fname} from {url}")
            downloaded = True
            break
        except Exception:
            pass
    if not downloaded:
        # Check theme images
        theme_url = f'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/images/{fname}'
        try:
            req = urllib.request.Request(theme_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                with open(os.path.join('assets', 'images', fname), 'wb') as out:
                    out.write(resp.read())
            print(f"Successfully downloaded {fname} from {theme_url}")
        except Exception as e:
            print(f"Could not find {fname}: {e}")
