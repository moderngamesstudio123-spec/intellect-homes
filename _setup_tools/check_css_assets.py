import re
import urllib.parse
import os
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0'}

with open('assets/css/custom.css', 'r', encoding='utf-8', errors='ignore') as f:
    css = f.read()

urls = re.findall(r'url\(["\']?([^"\'\)]+)["\']?\)', css)
print("URLs in custom.css:", len(urls))
for u in set(urls):
    print(" ", u)
    if not u.startswith('data:') and not u.startswith('assets/'):
        if u.startswith('//'):
            full_url = 'https:' + u
        elif u.startswith('/'):
            full_url = 'https://intellecthomes.com.au' + u
        elif u.startswith('../'):
            full_url = 'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/' + u.replace('../', '')
        else:
            full_url = 'https://intellecthomes.com.au/wp-content/themes/IntellectHomes/css/' + u
        
        parsed = urllib.parse.urlparse(full_url)
        fname = os.path.basename(parsed.path)
        dest = os.path.join('assets', 'images', fname)
        if not os.path.exists(dest):
            try:
                req = urllib.request.Request(full_url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    with open(dest, 'wb') as out:
                        out.write(resp.read())
                print(f"Downloaded css asset: {fname}")
            except Exception as e:
                print(f"Failed css asset {full_url}: {e}")
