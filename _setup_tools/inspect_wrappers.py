with open('raw_pages/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

header_pos = html.find('<header')
footer_pos = html.find('</footer>')

print("--- BEFORE HEADER ---")
print(html[:header_pos])

print("--- AFTER FOOTER ---")
print(html[footer_pos + len('</footer>'):])
