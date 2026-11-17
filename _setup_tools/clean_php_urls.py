import glob
import re

pages = [
    'about-us',
    'home-designs',
    'contact-us',
    'facades',
    'floor-plan',
    'gallery',
    'blogs',
    'calculator',
    'inclusions',
    'knockdown-rebuild',
]

for php_file in sorted(glob.glob('*.php')):
    if php_file == 'send-mail.php':
        continue
    with open(php_file, 'r', encoding='utf-8') as f:
        orig = f.read()
    updated = orig
    # Replace index.php links with /
    updated = re.sub(r'href="index\.php(#[^"]*)?"', lambda m: f'href="/{m.group(1) or ""}"', updated)
    updated = re.sub(r"href='index\.php(#[^']*)?'", lambda m: f"href='/{m.group(1) or ''}'", updated)
    # Replace page.php links with /page
    for p in pages:
        updated = re.sub(rf'href="{p}\.php(#[^"]*)?"', lambda m, p=p: f'href="/{p}{m.group(1) or ""}"', updated)
        updated = re.sub(rf"href='{p}\.php(#[^']*)?'", lambda m, p=p: f"href='/{p}{m.group(1) or ''}'", updated)
    if updated != orig:
        with open(php_file, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"Updated clean URLs in: {php_file}")
