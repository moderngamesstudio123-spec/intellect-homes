import re

with open('includes/header.php', 'r', encoding='utf-8') as f:
    header = f.read()

# Add base_path check
header = header.replace('<?php\nif (!isset($page_title)) {', '<?php\nif (!isset($base_path)) {\n    $base_path = "";\n}\nif (!isset($page_title)) {')

# Prepend base_path to assets/
header = header.replace('href="assets/', 'href="<?php echo $base_path; ?>assets/')
header = header.replace('src="assets/', 'src="<?php echo $base_path; ?>assets/')

# Prepend base_path to navigation links
nav_links = ['index.php', 'about-us.php', 'home-designs.php', 'facades.php', 'floor-plan.php', 'gallery.php', 'blogs.php', 'contact-us.php']
for nl in nav_links:
    header = header.replace(f'href="{nl}"', f'href="<?php echo $base_path; ?>{nl}"')

with open('includes/header.php', 'w', encoding='utf-8') as f:
    f.write(header)

with open('includes/footer.php', 'r', encoding='utf-8') as f:
    footer = f.read()

footer = footer.replace('src="assets/', 'src="<?php echo $base_path; ?>assets/')
footer = footer.replace('href="assets/', 'href="<?php echo $base_path; ?>assets/')
for nl in nav_links:
    footer = footer.replace(f'href="{nl}"', f'href="<?php echo $base_path; ?>{nl}"')

with open('includes/footer.php', 'w', encoding='utf-8') as f:
    f.write(footer)

# Now in subfolders home-design and blog, ensure $base_path = "../";
import os
for folder in ['home-design', 'blog']:
    for f in os.listdir(folder):
        if f.endswith('.php'):
            fpath = os.path.join(folder, f)
            with open(fpath, 'r', encoding='utf-8') as pf:
                code = pf.read()
            if '$base_path' not in code:
                code = code.replace('<?php', '<?php\n$base_path = "../";', 1)
                with open(fpath, 'w', encoding='utf-8') as pf:
                    pf.write(code)

print("Dynamic $base_path applied to header, footer, and subfolder pages!")
