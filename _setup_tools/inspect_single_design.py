import urllib.request
import re

url = 'https://intellecthomes.com.au/home-design/16-vivero-wyndham-vale-vic-3024/'
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

h_end = html.find('</header>') + len('</header>')
f_start = html.find('<footer')
print("Body length:", f_start - h_end)
print(html[h_end:h_end+1000])
