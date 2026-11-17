import glob
import os

rename_map = {
    'index.html': 'index.php',
    'about.html': 'about-us.php',
    'designs.html': 'home-designs.php',
    'contact.html': 'contact-us.php',
    'facades.html': 'facades.php',
    'floor-plan.html': 'floor-plan.php',
    'gallery.html': 'gallery.php',
    'blogs.html': 'blogs.php',
    'calculator.html': 'calculator.php',
    'inclusions.html': 'inclusions.php',
    'knockdown-rebuild.html': 'knockdown-rebuild.php',
}

link_replacements = [
    ('href="index.html', 'href="index.php'),
    ('href="about.html', 'href="about-us.php'),
    ('href="designs.html', 'href="home-designs.php'),
    ('href="contact.html', 'href="contact-us.php'),
    ('href="facades.html', 'href="facades.php'),
    ('href="floor-plan.html', 'href="floor-plan.php'),
    ('href="gallery.html', 'href="gallery.php'),
    ('href="blogs.html', 'href="blogs.php'),
    ('href="calculator.html', 'href="calculator.php'),
    ('href="inclusions.html', 'href="inclusions.php'),
    ('href="knockdown-rebuild.html', 'href="knockdown-rebuild.php'),
    ("'index.html", "'index.php"),
    ("'about.html", "'about-us.php"),
    ("'designs.html", "'home-designs.php"),
    ("'contact.html", "'contact-us.php"),
    ("'facades.html", "'facades.php"),
    ("'floor-plan.html", "'floor-plan.php"),
    ("'gallery.html", "'gallery.php"),
    ("'blogs.html", "'blogs.php"),
    ("'calculator.html", "'calculator.php"),
    ("'inclusions.html", "'inclusions.php"),
    ("'knockdown-rebuild.html", "'knockdown-rebuild.php"),
]

for old_file, new_file in rename_map.items():
    if not os.path.exists(old_file):
        print(f"Missing {old_file}, skipping")
        continue
    with open(old_file, 'r', encoding='utf-8') as f:
        content = f.read()
    for old_link, new_link in link_replacements:
        content = content.replace(old_link, new_link)
    with open(new_file, 'w', encoding='utf-8') as f:
        f.write(content)
    os.remove(old_file)
    print(f"Converted: {old_file} -> {new_file}")

# Also update any references in assets/js/main.js
if os.path.exists('assets/js/main.js'):
    with open('assets/js/main.js', 'r', encoding='utf-8') as f:
        js = f.read()
    new_js = js
    for old_link, new_link in link_replacements:
        new_js = new_js.replace(old_link, new_link)
    if new_js != js:
        with open('assets/js/main.js', 'w', encoding='utf-8') as f:
            f.write(new_js)
        print("Updated links in assets/js/main.js")
