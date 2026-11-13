import urllib.request
import re

req = urllib.request.Request('https://intellecthomes.com.au/', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

# print all modals
modals = re.findall(r'<div[^>]*class=["\'][^"\']*modal[^"\']*["\'][^>]*>.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
for m in modals:
    print("MODAL:")
    print(m)

# print any floating or fixed buttons
fixed = re.findall(r'<[^>]+(?:floating|fixed|sticky|chat|whatsapp|quick-contact)[^>]*>.*?</[^>]+>', html, re.DOTALL | re.IGNORECASE)
for f in fixed:
    print("FIXED/FLOATING:")
    print(f[:300])

