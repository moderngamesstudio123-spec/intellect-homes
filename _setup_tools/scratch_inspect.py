import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def get_url(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8', errors='ignore')

# Check sitemap
for sm_url in ['https://intellecthomes.com.au/sitemap.xml', 'https://intellecthomes.com.au/wp-sitemap.xml', 'https://intellecthomes.com.au/sitemap_index.xml']:
    try:
        content = get_url(sm_url)
        print(f"Found sitemap at {sm_url}: {len(content)} bytes")
        locs = re.findall(r'<loc>(.*?)</loc>', content)
        print("Sitemap locs:", locs[:10])
    except Exception as e:
        print(f"No sitemap at {sm_url}: {e}")

# Fetch home page
html = get_url('https://intellecthomes.com.au/')
nav_links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', html)
site_links = set()
for l in nav_links:
    if 'intellecthomes.com.au' in l or (l.startswith('/') and not l.startswith('//')):
        site_links.add(l)

print("Found internal links:")
for l in sorted(site_links):
    print(" -", l)
