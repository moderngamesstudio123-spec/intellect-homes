import urllib.request
import re

url = 'https://intellecthomes.com.au/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

title = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
if title:
    print('Title:', title.group(1))

css = re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', html)
print(f'Stylesheets ({len(css)}):')
for c in css:
    print(' ', c)

scripts = re.findall(r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']', html)
print(f'Scripts ({len(scripts)}):')
for s in scripts:
    print(' ', s)
