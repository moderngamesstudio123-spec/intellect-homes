import re

with open('index.php', 'r', encoding='utf-8') as f:
    text = f.read()

i_tags = re.findall(r'<i[^>]*>.*?</i>', text, re.DOTALL)
print("i tags in index.php:")
for it in set(i_tags):
    print(" ", it)

img_icons = [img for img in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', text) if 'icon' in img or 'svg' in img]
print("img icons in index.php:")
for img in set(img_icons):
    print(" ", img)

