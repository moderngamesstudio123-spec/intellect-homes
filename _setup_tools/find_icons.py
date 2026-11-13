import re

for filename in ['includes/header.php', 'includes/footer.php', 'index.php', 'contact-us.php']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    icons = re.findall(r'(<[^>]+(?:class=[\'"][^\'"]*(?:fa-|icon)[^\'"]*[\'"]|src=[\'"][^\'"]*icon[^\'"]*[\'"])[^>]*>.*?)(?=<\w|$)', content)
    print(f"=== {filename} ({len(icons)} icons) ===")
    for ic in icons:
        # print snippet
        clean = ic.strip()[:100]
        print("  ", clean)

