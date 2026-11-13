import re

pages = ['index', 'about-us', 'home-designs', 'facades', 'floor-plan', 'gallery', 'blogs', 'contact-us']

for p in pages:
    with open(f'raw_pages/{p}.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    header_m = re.search(r'<header.*?</header>', html, re.DOTALL | re.IGNORECASE)
    footer_m = re.search(r'<footer.*?</footer>', html, re.DOTALL | re.IGNORECASE)
    print(f"Page {p}: Header={len(header_m.group(0)) if header_m else 0}, Footer={len(footer_m.group(0)) if footer_m else 0}")
