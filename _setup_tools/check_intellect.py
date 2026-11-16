import glob
import re

for f in sorted(glob.glob('*.html')):
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.I)
    if not m:
        continue
    body = m.group(1)
    body_clean = re.sub(r'<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>', ' ', body, flags=re.DOTALL | re.I)
    for line in body_clean.splitlines():
        stripped = re.sub(r'<span[^>]*class=["\'][^"\']*text-gold[^"\']*["\'][^>]*>.*?</span>', '', line, flags=re.I)
        stripped = re.sub(r'<span[^>]*color:\s*(?:#DF982B|#D4AF37|var\(--accent-gold\))[^>]*>.*?</span>', '', stripped, flags=re.I)
        stripped = re.sub(r'<[^>]+>', ' ', stripped)
        # ignore email addresses like admin@intellecthomes.com.au
        stripped_no_email = re.sub(r'admin@intellecthomes\.com\.au', '', stripped, flags=re.I)
        if re.search(r'intellect', stripped_no_email, re.I):
            print(f'{f}: {stripped_no_email.strip()[:140]}')
