import os
import urllib.request
import urllib.parse
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def download_file(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(local_path, 'wb') as f:
                f.write(data)
        print(f"Downloaded: {url} -> {local_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {url}: {e}")

# 1. Download CSS
css_files = [
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/style.css',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/css/bootstrap.min.css',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/css/slicknav.min.css',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/css/swiper-bundle.min.css',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/css/all.min.css',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/css/animate.css',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/css/magnific-popup.css',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/css/custom.css'
]

for url in css_files:
    fname = os.path.basename(urllib.parse.urlparse(url).path)
    download_file(url, os.path.join('assets', 'css', fname))

# 2. Download JS
js_files = [
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/jquery-3.7.1.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/bootstrap.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/validator.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/jquery.slicknav.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/swiper-bundle.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/jquery.waypoints.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/jquery.counterup.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/jquery.magnific-popup.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/SmoothScroll.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/parallaxie.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/gsap.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/magiccursor.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/splitType.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/ScrollTrigger.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/jquery.mb.YTPlayer.min.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/wow.js',
    'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/js/function.js'
]

for url in js_files:
    fname = os.path.basename(urllib.parse.urlparse(url).path)
    download_file(url, os.path.join('assets', 'js', fname))

# Check fontawesome webfonts in all.min.css
all_css_path = os.path.join('assets', 'css', 'all.min.css')
if os.path.exists(all_css_path):
    with open(all_css_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        fonts = set(re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', content))
        print("Font references in all.min.css:", fonts)
        for font in fonts:
            font_clean = font.split('?')[0].split('#')[0]
            if font_clean.startswith('../webfonts/'):
                font_name = font_clean.replace('../webfonts/', '')
                font_url = f'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/webfonts/{font_name}'
                download_file(font_url, os.path.join('assets', 'webfonts', font_name))
