import re

with open('raw_pages/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

videos = re.findall(r'<video[^>]+src=["\']([^"\']+)["\']', html)
source_videos = re.findall(r'<source[^>]+src=["\']([^"\']+)["\']', html)
print("Videos found:", videos + source_videos)
