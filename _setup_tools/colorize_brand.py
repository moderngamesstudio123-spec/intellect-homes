import glob
import re

def colorize_body(html):
    m = re.search(r'(<body[^>]*>)(.*)(</body>)', html, re.DOTALL | re.IGNORECASE)
    if not m:
        return html
    head_part = html[:m.start(2)]
    body_part = m.group(2)
    tail_part = html[m.end(2):]

    body_part = body_part.replace(
        '<span style="display: block; font-size: 1.15rem; color: #FFFFFF;">Intellect Homes</span>',
        '<span style="display: block; font-size: 1.15rem; color: var(--accent-gold);">Intellect Homes</span>'
    )
    body_part = body_part.replace(
        '<span style="font-family: var(--font-heading); font-weight: 800; font-size: 1.25rem; color: #fff;">INTELLECT HOMES</span>',
        '<span style="font-family: var(--font-heading); font-weight: 800; font-size: 1.25rem; color: var(--accent-gold);">INTELLECT HOMES</span>'
    )

    tokens = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)', body_part, flags=re.DOTALL | re.IGNORECASE)
    out = []
    skip_next_text = False
    for tok in tokens:
        if tok.startswith('<'):
            out.append(tok)
            if re.search(r'class=["\'][^"\']*text-gold|color:\s*(?:#DF982B|#D4AF37|var\(--accent-gold\))', tok, re.I):
                skip_next_text = True
            else:
                skip_next_text = False
        else:
            if skip_next_text:
                out.append(tok)
            else:
                new_tok = re.sub(r'(Intellect\s+Homes)', r'<span class="text-gold">\1</span>', tok, flags=re.IGNORECASE)
                out.append(new_tok)
            skip_next_text = False

    return head_part + ''.join(out) + tail_part

for f in sorted(glob.glob('*.html')):
    with open(f, 'r', encoding='utf-8') as fh:
        orig = fh.read()
    updated = colorize_body(orig)
    if updated != orig:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(updated)
        print('Updated:', f)
