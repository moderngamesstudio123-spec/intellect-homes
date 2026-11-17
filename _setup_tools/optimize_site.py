import glob
import os
import re
from PIL import Image, ImageOps

# 1. Optimize large JPG/JPEG images in assets/images/
saved_bytes = 0
for path in sorted(glob.glob('assets/images/*')):
    ext = os.path.splitext(path)[1].lower()
    if ext not in ('.jpg', '.jpeg'):
        continue
    orig_size = os.path.getsize(path)
    if orig_size < 100 * 1024:
        continue
    try:
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            w, h = img.size
            if w > 1600:
                new_h = int(h * (1600 / w))
                img = img.resize((1600, new_h), Image.Resampling.LANCZOS)
            tmp_path = path + '.tmp.jpg'
            img.save(tmp_path, format='JPEG', quality=82, optimize=True, progressive=True)
        new_size = os.path.getsize(tmp_path)
        if new_size < orig_size:
            os.replace(tmp_path, path)
            diff = (orig_size - new_size) / 1024
            saved_bytes += (orig_size - new_size)
            print(f"Compressed {os.path.basename(path)}: {orig_size/1024:.0f} KB -> {new_size/1024:.0f} KB (-{diff:.0f} KB)")
        else:
            os.remove(tmp_path)
    except Exception as e:
        print(f"Skipped {path}: {e}")

print(f"\nTotal image size reduced by: {saved_bytes / 1024:.0f} KB ({saved_bytes / (1024*1024):.2f} MB)\n")

# 2. Add loading="lazy" decoding="async" to below-the-fold images and defer main.js across all root .php pages
eager_markers = ('assets/images/logo.webp', 'assets/images/bpc-primary.png', 'assets/images/slider-modern-facade.jpg')

def optimize_img_tag(m):
    tag = m.group(0)
    if any(em in tag for em in eager_markers):
        if 'slider-modern-facade.jpg' in tag and 'fetchpriority=' not in tag:
            tag = tag[:-1] + ' fetchpriority="high" decoding="async">'
        elif 'decoding=' not in tag:
            tag = tag[:-1] + ' decoding="async">'
        return tag
    if 'loading=' not in tag.lower():
        tag = tag[:-1] + ' loading="lazy" decoding="async">'
    elif 'decoding=' not in tag.lower():
        tag = tag[:-1] + ' decoding="async">'
    return tag

for php_file in sorted(glob.glob('*.php')):
    if php_file == 'send-mail.php':
        continue
    with open(php_file, 'r', encoding='utf-8') as f:
        orig = f.read()
    updated = re.sub(r'<img\b[^>]*>', optimize_img_tag, orig, flags=re.I)
    updated = updated.replace('<script src="assets/js/main.js"></script>', '<script src="assets/js/main.js" defer></script>')
    if updated != orig:
        with open(php_file, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"Optimized HTML tags in: {php_file}")
