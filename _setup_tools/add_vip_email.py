import glob

target = '''        <a href="tel:+61411560177" class="vip-action-btn vip-call-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Direct Phone: 0411 560 177
        </a>'''

replacement = target + '''

        <a href="mailto:admin@intellecthomes.com.au" class="vip-action-btn vip-call-btn" style="color: #DF982B; border-color: rgba(223, 152, 43, 0.35);">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          Email: admin@intellecthomes.com.au
        </a>'''

for f in sorted(glob.glob('*.html')):
    with open(f, 'r', encoding='utf-8') as fh:
        txt = fh.read()
    idx = txt.find('vip-concierge-widget')
    if idx == -1:
        continue
    if target in txt and 'mailto:admin@intellecthomes.com.au' not in txt[idx:]:
        new_txt = txt.replace(target, replacement, 1)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_txt)
        print('Updated:', f)
    else:
        print('Skipped or pattern mismatch:', f)
