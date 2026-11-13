import os
import re

design_slugs = [
    '4-conservation-drive-tarneit-vic-3029',
    '4-geller-circuit-tarneit-vic-3029',
    '170-cravens-road-mernda-vic-3754',
    '5-cubitt-cres-tarneit-vic-3029',
    '7-abbington-drive-truganina',
    '193-callway-street-mambourin',
    '16-vivero-wyndham-vale-vic-3024',
    '21-oswald-street-dandenong-3175'
]

blog_slugs = [
    'granny-flats-vs-new-homes-what-should-you-build',
    'why-choose-a-knock-down-rebuild-instead-of-renovating',
    '7-benefits-of-building-a-granny-flat-in-australia'
]

def update_file(filepath, is_subfolder=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Prefix for assets if in subfolder
    prefix = '../' if is_subfolder else ''
    
    # Fix home design links
    for slug in design_slugs:
        # replace https://intellecthomes.com.au/home-design/{slug}/
        content = re.sub(rf'https?://intellecthomes\.com\.au/home-design/{slug}/?', f'{prefix}home-design/{slug}.php', content)
        content = re.sub(rf'href=["\']/home-design/{slug}/?["\']', f'href="{prefix}home-design/{slug}.php"', content)

    # Fix blog links
    for slug in blog_slugs:
        content = re.sub(rf'https?://intellecthomes\.com\.au/{slug}/?', f'{prefix}blog/{slug}.php', content)
        content = re.sub(rf'href=["\']/{slug}/?["\']', f'href="{prefix}blog/{slug}.php"', content)

    # Fix generic links
    content = content.replace('https://intellecthomes.com.au/property/', f'{prefix}home-designs.php')
    content = content.replace('https://intellecthomes.com.au/blog/', f'{prefix}blogs.php')
    content = content.replace('https://intellecthomes.com.au/category/granny-flats/', f'{prefix}home-designs.php')
    content = content.replace('https://intellecthomes.com.au/category/knock-down-rebuild/', f'{prefix}home-designs.php')
    content = content.replace('https://intellecthomes.com.au/category/new-construction/', f'{prefix}home-designs.php')
    content = content.replace('https://intellecthomes.com.au/category/uncategorized/', f'{prefix}blogs.php')

    # If subfolder, adjust assets path in body
    if is_subfolder:
        content = content.replace('src="assets/', 'src="../assets/')
        content = content.replace("src='assets/", "src='../assets/")
        content = content.replace('href="assets/', 'href="../assets/')
        content = content.replace('url(assets/', 'url(../assets/')
        content = content.replace('url("assets/', 'url("../assets/')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update root php files
root_php = [f for f in os.listdir('.') if f.endswith('.php')]
for f in root_php:
    update_file(f, is_subfolder=False)

# Update includes
update_file('includes/header.php', is_subfolder=False)
update_file('includes/footer.php', is_subfolder=False)

# Update subfolders
for f in os.listdir('home-design'):
    if f.endswith('.php'):
        update_file(os.path.join('home-design', f), is_subfolder=True)

for f in os.listdir('blog'):
    if f.endswith('.php'):
        update_file(os.path.join('blog', f), is_subfolder=True)

print("All links updated across all PHP files!")
