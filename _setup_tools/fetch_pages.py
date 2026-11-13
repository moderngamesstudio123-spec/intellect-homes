import urllib.request
import re
import os

pages = {
    'index': 'https://intellecthomes.com.au/',
    'about-us': 'https://intellecthomes.com.au/about-us/',
    'home-designs': 'https://intellecthomes.com.au/home-designs/',
    'facades': 'https://intellecthomes.com.au/facades/',
    'floor-plan': 'https://intellecthomes.com.au/floor-plan/',
    'gallery': 'https://intellecthomes.com.au/gallery/',
    'blogs': 'https://intellecthomes.com.au/blogs/',
    'contact-us': 'https://intellecthomes.com.au/contact-us/',
    'thank-you': 'https://intellecthomes.com.au/thank-you/'
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

os.makedirs('raw_pages', exist_ok=True)

for name, url in pages.items():
    print(f"Fetching {name} from {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            with open(f'raw_pages/{name}.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f" Saved {name}.html ({len(content)} bytes)")
    except Exception as e:
        print(f" Error fetching {name}: {e}")
