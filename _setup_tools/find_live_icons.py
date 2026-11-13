import urllib.request
import re

headers = {'User-Agent': 'Mozilla/5.0'}
for p in ['', 'home-designs/', 'about-us/', 'facades/', 'floor-plan/', 'gallery/', 'blogs/', 'contact-us/']:
    url = f'https://intellecthomes.com.au/{p}'
    try:
        html = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read().decode('utf-8', errors='ignore')
        svgs = re.findall(r'<svg[^>]*>.*?</svg>', html, re.DOTALL)
        if len(svgs) > 1:
            print(url, 'has svgs:', len(svgs))
            for s in svgs:
                print('  SVG:', s[:100])
        icons = re.findall(r'<i\s+class=["\']([^"\']+)["\']', html)
        msg_icons = [i for i in icons if any(w in i for w in ['message', 'envelope', 'comment', 'mail'])]
        if msg_icons:
            print(url, 'msg icons:', msg_icons)
    except Exception as e:
        print(url, e)

