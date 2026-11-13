import re

with open('raw_pages/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's see what major header and footer tags exist
print("Header search:")
header_m = re.search(r'(<header.*?</header>)', html, re.DOTALL | re.IGNORECASE)
if header_m:
    print(f"Found <header> tag, length {len(header_m.group(1))}")
    print(header_m.group(1)[:500])
else:
    print("No <header> tag found, looking for <nav> or top bar...")

footer_m = re.search(r'(<footer.*?</footer>)', html, re.DOTALL | re.IGNORECASE)
if footer_m:
    print(f"Found <footer> tag, length {len(footer_m.group(1))}")
    print(footer_m.group(1)[:500])
else:
    print("No <footer> tag found")
