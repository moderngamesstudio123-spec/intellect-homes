import glob
import re

def replace_100_in_text(html):
    m = re.search(r'(<body[^>]*>)(.*)(</body>)', html, re.DOTALL | re.IGNORECASE)
    if not m:
        return html
    head = html[:m.start(2)]
    body = m.group(2)
    tail = html[m.end(2):]

    tokens = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)', body, flags=re.DOTALL | re.IGNORECASE)
    out = []
    for tok in tokens:
        if tok.startswith('<'):
            out.append(tok)
        else:
            out.append(tok.replace('100%', 'Transparency'))
    return head + ''.join(out) + tail

for f in sorted(glob.glob('*.html')):
    with open(f, 'r', encoding='utf-8') as fh:
        orig = fh.read()
    updated = replace_100_in_text(orig)
    if updated != orig:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(updated)
        print('Updated:', f)
