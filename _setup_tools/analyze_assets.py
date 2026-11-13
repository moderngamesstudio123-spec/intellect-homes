import re
import os
import urllib.parse

html_files = [os.path.join('raw_pages', f) for f in os.listdir('raw_pages') if f.endswith('.html')]

css_urls = set()
js_urls = set()
img_urls = set()

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSS
    for m in re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', content):
        css_urls.add(m)
    # JS
    for m in re.findall(r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']', content):
        js_urls.add(m)
    # Images in img src
    for m in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content):
        img_urls.add(m)
    # background images in style
    for m in re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', content):
        img_urls.add(m)

print(f"Total CSS files: {len(css_urls)}")
for c in sorted(css_urls):
    print("  CSS:", c)

print(f"\nTotal JS files: {len(js_urls)}")
for j in sorted(js_urls):
    print("  JS:", j)

print(f"\nTotal Image/Media URLs: {len(img_urls)}")
