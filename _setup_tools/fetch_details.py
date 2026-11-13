import urllib.request
import re
import os
import json

headers = {'User-Agent': 'Mozilla/5.0'}

with open('image_mapping.json', 'r', encoding='utf-8') as f:
    img_map = json.load(f)

sorted_img_urls = sorted(img_map.keys(), key=lambda x: len(x), reverse=True)

def replace_links_and_assets(content):
    for url in sorted_img_urls:
        local_path = img_map[url]
        content = content.replace(url, local_path)
    content = re.sub(r'https?://intellecthomes\.com\.au/wp-content/uploads/[0-9/]+/([^"\'\s>]+)', r'assets/images/\1', content)
    content = re.sub(r'https?://intellecthomes\.com\.au/wp-content/themes/IntellectHomes/images/([^"\'\s>]+)', r'assets/images/\1', content)
    page_link_map = [
        ('https://intellecthomes.com.au/about-us/', 'about-us.php'),
        ('https://intellecthomes.com.au/about-us', 'about-us.php'),
        ('https://intellecthomes.com.au/home-designs/', 'home-designs.php'),
        ('https://intellecthomes.com.au/home-designs', 'home-designs.php'),
        ('https://intellecthomes.com.au/facades/', 'facades.php'),
        ('https://intellecthomes.com.au/facades', 'facades.php'),
        ('https://intellecthomes.com.au/floor-plan/', 'floor-plan.php'),
        ('https://intellecthomes.com.au/floor-plan', 'floor-plan.php'),
        ('https://intellecthomes.com.au/gallery/', 'gallery.php'),
        ('https://intellecthomes.com.au/gallery', 'gallery.php'),
        ('https://intellecthomes.com.au/blogs/', 'blogs.php'),
        ('https://intellecthomes.com.au/blogs', 'blogs.php'),
        ('https://intellecthomes.com.au/contact-us/', 'contact-us.php'),
        ('https://intellecthomes.com.au/contact-us', 'contact-us.php'),
        ('https://intellecthomes.com.au/thank-you/', 'thank-you.php'),
        ('https://intellecthomes.com.au/thank-you', 'thank-you.php'),
        ('https://intellecthomes.com.au/', 'index.php'),
        ('https://intellecthomes.com.au', 'index.php'),
    ]
    for orig, rep in page_link_map:
        content = content.replace(f'href="{orig}"', f'href="{rep}"')
        content = content.replace(f"href='{orig}'", f"href='{rep}'")
    return content

# 8 Home designs
designs = [
    ('4-conservation-drive-tarneit-vic-3029', 'https://intellecthomes.com.au/home-design/4-conservation-drive-tarneit-vic-3029/'),
    ('4-geller-circuit-tarneit-vic-3029', 'https://intellecthomes.com.au/home-design/4-geller-circuit-tarneit-vic-3029/'),
    ('170-cravens-road-mernda-vic-3754', 'https://intellecthomes.com.au/home-design/170-cravens-road-mernda-vic-3754/'),
    ('5-cubitt-cres-tarneit-vic-3029', 'https://intellecthomes.com.au/home-design/5-cubitt-cres-tarneit-vic-3029/'),
    ('7-abbington-drive-truganina', 'https://intellecthomes.com.au/home-design/7-abbington-drive-truganina/'),
    ('193-callway-street-mambourin', 'https://intellecthomes.com.au/home-design/193-callway-street-mambourin/'),
    ('16-vivero-wyndham-vale-vic-3024', 'https://intellecthomes.com.au/home-design/16-vivero-wyndham-vale-vic-3024/'),
    ('21-oswald-street-dandenong-3175', 'https://intellecthomes.com.au/home-design/21-oswald-street-dandenong-3175/')
]

os.makedirs('home-design', exist_ok=True)

for slug, url in designs:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        h_end = html.find('</header>') + len('</header>')
        f_start = html.find('<footer')
        body = html[h_end:f_start].strip()
        body = replace_links_and_assets(body)

        title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
        title = title_m.group(1).replace(' - Intellecthomes', '').strip() if title_m else slug

        php_content = f"""<?php
$page_title = "{title} | Intellect Homes";
$current_page = "designs";
require_once __DIR__ . '/../includes/header.php';
?>

{body}

<?php
require_once __DIR__ . '/../includes/footer.php';
?>
"""
        with open(f'home-design/{slug}.php', 'w', encoding='utf-8') as f:
            f.write(php_content)
        print(f"Created home-design/{slug}.php")
    except Exception as e:
        print(f"Failed {slug}: {e}")

# 3 Blog posts
blogs = [
    ('granny-flats-vs-new-homes-what-should-you-build', 'https://intellecthomes.com.au/granny-flats-vs-new-homes-what-should-you-build/'),
    ('why-choose-a-knock-down-rebuild-instead-of-renovating', 'https://intellecthomes.com.au/why-choose-a-knock-down-rebuild-instead-of-renovating/'),
    ('7-benefits-of-building-a-granny-flat-in-australia', 'https://intellecthomes.com.au/7-benefits-of-building-a-granny-flat-in-australia/')
]

os.makedirs('blog', exist_ok=True)

for slug, url in blogs:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        h_end = html.find('</header>') + len('</header>')
        f_start = html.find('<footer')
        body = html[h_end:f_start].strip()
        body = replace_links_and_assets(body)

        title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
        title = title_m.group(1).replace(' - Intellecthomes', '').strip() if title_m else slug

        php_content = f"""<?php
$page_title = "{title} | Intellect Homes";
$current_page = "blogs";
require_once __DIR__ . '/../includes/header.php';
?>

{body}

<?php
require_once __DIR__ . '/../includes/footer.php';
?>
"""
        with open(f'blog/{slug}.php', 'w', encoding='utf-8') as f:
            f.write(php_content)
        print(f"Created blog/{slug}.php")
    except Exception as e:
        print(f"Failed blog {slug}: {e}")
