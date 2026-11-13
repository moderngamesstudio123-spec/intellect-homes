import os
import re
import urllib.parse
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

html_dir = 'raw_pages'
all_imgs = set()

for fname in os.listdir(html_dir):
    if not fname.endswith('.html'):
        continue
    with open(os.path.join(html_dir, fname), 'r', encoding='utf-8') as f:
        html = f.read()

    # Find img tags
    for src in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html):
        all_imgs.add(src)
    
    # Find background images or inline styles
    for src in re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', html):
        if not src.startswith('data:') and not '.css' in src and not '.woff' in src:
            all_imgs.add(src)

    # Find favicon or shortcut icons
    for src in re.findall(r'<link[^>]+rel=["\'](?:shortcut )?icon["\'][^>]+href=["\']([^"\']+)["\']', html):
        all_imgs.add(src)

print(f"Total unique images found across all pages: {len(all_imgs)}")

os.makedirs('assets/images', exist_ok=True)

url_mapping = {}

for img_url in all_imgs:
    if img_url.startswith('//'):
        full_url = 'https:' + img_url
    elif img_url.startswith('/'):
        full_url = 'https://intellecthomes.com.au' + img_url
    elif not img_url.startswith('http'):
        full_url = 'https://intellecthomes.com.au/' + img_url
    else:
        full_url = img_url

    parsed = urllib.parse.urlparse(full_url)
    basename = os.path.basename(parsed.path)
    if not basename:
        continue
    
    # Clean query strings from basename
    basename = basename.split('?')[0]
    local_path = os.path.join('assets', 'images', basename)
    
    url_mapping[img_url] = f'assets/images/{basename}'
    
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        continue
    
    try:
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(local_path, 'wb') as f:
                f.write(data)
        print(f"Downloaded: {basename} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {full_url}: {e}")

import json
with open('image_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(url_mapping, f, indent=2)

print("Image mapping saved to image_mapping.json")
