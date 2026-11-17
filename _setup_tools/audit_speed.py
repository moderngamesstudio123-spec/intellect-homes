import urllib.request
import time
import re
import os

url = 'https://intellect-homes.vercel.app/'
t0 = time.time()
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode('utf-8', errors='ignore')
t1 = time.time()
print(f'HTML TTFB + download: {(t1 - t0) * 1000:.0f} ms | Size: {len(html) / 1024:.1f} KB')

imgs = set(re.findall(r'assets/images/[^"\'\s>]+', html))
total_img_kb = 0
large_imgs = []
for img in imgs:
    if os.path.exists(img):
        sz = os.path.getsize(img) / 1024
        total_img_kb += sz
        if sz > 120:
            large_imgs.append((img, sz))
print(f'Images on Home: {len(imgs)} files | Total size: {total_img_kb / 1024:.2f} MB')
for li, sz in sorted(large_imgs, key=lambda x: -x[1]):
    print(f'  Large image: {li} ({sz:.0f} KB)')

css_sz = os.path.getsize('assets/css/style.css') / 1024
js_sz = os.path.getsize('assets/js/main.js') / 1024
print(f'CSS: {css_sz:.1f} KB | JS: {js_sz:.1f} KB')

# Check lazy loading on below-the-fold images
img_tags = re.findall(r'<img\b[^>]*>', html, re.I)
lazy_count = sum(1 for t in img_tags if 'loading="lazy"' in t.lower())
print(f'Total <img> tags: {len(img_tags)} | With loading="lazy": {lazy_count}')
