import os
import re
import json

os.makedirs('includes', exist_ok=True)

# Load image mapping
with open('image_mapping.json', 'r', encoding='utf-8') as f:
    img_map = json.load(f)

# Sort mapping by length descending to avoid partial replacements
sorted_img_urls = sorted(img_map.keys(), key=lambda x: len(x), reverse=True)

def replace_links_and_assets(content):
    # 1. Replace assets/images
    for url in sorted_img_urls:
        local_path = img_map[url]
        content = content.replace(url, local_path)
    
    # Also replace any remaining wp-content uploads or theme links
    content = re.sub(r'https?://intellecthomes\.com\.au/wp-content/uploads/[0-9/]+/([^"\'\s>]+)', r'assets/images/\1', content)
    content = re.sub(r'https?://intellecthomes\.com\.au/wp-content/themes/IntellectHomes/images/hero\.mp4', 'assets/images/hero.mp4', content)
    content = re.sub(r'https?://intellecthomes\.com\.au/wp-content/themes/IntellectHomes/images/([^"\'\s>]+)', r'assets/images/\1', content)

    # 2. Replace internal page links
    page_link_map = [
        ('https://intellecthomes.com.au/about-us/', 'about-us.php'),
        ('https://intellecthomes.com.au/about-us', 'about-us.php'),
        ('https://intellecthomes.com.au/home-designs/', 'home-designs.php'),
        ('https://intellecthomes.com.au/home-designs', 'home-designs.php'),
        ('https://intellecthomes.com.au/facades/', 'facades.php'),
        ('https://intellecthomes.com.au/facades', 'facades.php'),
        ('https://intellecthomes.com.au/floor-plan/', 'floor-plan.php'),
        ('https://intellecthomes.com.au/floor-plan', 'floor-plan.php'),
        ('https://intellecthomes.com.au/gallery/', 'gallery.php'),
        ('https://intellecthomes.com.au/gallery', 'gallery.php'),
        ('https://intellecthomes.com.au/blogs/', 'blogs.php'),
        ('https://intellecthomes.com.au/blogs', 'blogs.php'),
        ('https://intellecthomes.com.au/contact-us/', 'contact-us.php'),
        ('https://intellecthomes.com.au/contact-us', 'contact-us.php'),
        ('https://intellecthomes.com.au/thank-you/', 'thank-you.php'),
        ('https://intellecthomes.com.au/thank-you', 'thank-you.php'),
        ('https://intellecthomes.com.au/', 'index.php'),
        ('https://intellecthomes.com.au', 'index.php'),
    ]
    for orig, rep in page_link_map:
        content = content.replace(f'href="{orig}"', f'href="{rep}"')
        content = content.replace(f"href='{orig}'", f"href='{rep}'")

    return content

# Read index.html for base header and footer extraction
with open('raw_pages/index.html', 'r', encoding='utf-8') as f:
    index_raw = f.read()

# Header: from start of <header to </header>
header_start = index_raw.find('<header')
header_end = index_raw.find('</header>') + len('</header>')
header_html = index_raw[header_start:header_end]
header_html = replace_links_and_assets(header_html)

# Add active class PHP tags to menu items
menu_items = [
    ('index.php', 'home'),
    ('about-us.php', 'about'),
    ('home-designs.php', 'designs'),
    ('facades.php', 'facades'),
    ('floor-plan.php', 'floor-plan'),
    ('gallery.php', 'gallery'),
    ('blogs.php', 'blogs'),
    ('contact-us.php', 'contact')
]

for php_file, key in menu_items:
    # replace href="xxx.php" with active check
    pattern = f'href="{php_file}"'
    replacement = f'href="{php_file}" class="<?php echo ($current_page == \'{key}\') ? \'nav-link active\' : \'nav-link\'; ?>"'
    # In navbar, class might already exist, so check
    header_html = header_html.replace(f'<a class="nav-link" href="{php_file}">', f'<a class="nav-link <?php echo ($current_page == \'{key}\') ? \'active\' : \'\'; ?>" href="{php_file}">')

# Make includes/header.php
header_php_content = """<?php
if (!isset($page_title)) {
    $page_title = "Intellect Homes | Custom Home Builder Victoria";
}
if (!isset($current_page)) {
    $current_page = "home";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo htmlspecialchars($page_title); ?></title>
    
    <!-- Favicon Icon -->
    <link rel="shortcut icon" type="image/x-icon" href="assets/images/android-chrome-192x192-1.webp">
    
    <!-- Google Fonts Css-->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
    
    <!-- Bootstrap Css -->
    <link rel="stylesheet" href="assets/css/bootstrap.min.css">
    <!-- SlickNav Css -->
    <link rel="stylesheet" href="assets/css/slicknav.min.css">
    <!-- Swiper Css -->
    <link rel="stylesheet" href="assets/css/swiper-bundle.min.css">
    <!-- Font Awesome Css -->
    <link rel="stylesheet" href="assets/css/all.min.css">
    <!-- Animate Css -->
    <link rel="stylesheet" href="assets/css/animate.css">
    <!-- Magnific Popup Core Css File -->
    <link rel="stylesheet" href="assets/css/magnific-popup.css">
    <!-- Main Custom Css -->
    <link rel="stylesheet" href="assets/css/custom.css">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="tt-magic-cursor">

    <!-- Preloader Start -->
    <div class="preloader">
        <div class="loading-container">
            <div class="loading"></div>
            <div id="loading-icon"><img src="assets/images/android-chrome-192x192-1.webp" alt="Loading"></div>
        </div>
    </div>
    <!-- Preloader End -->

    <!-- Magic Cursor Start -->
    <div id="magic-cursor">
        <div id="ball"></div>
    </div>
    <!-- Magic Cursor End -->

""" + header_html + "\n"

with open('includes/header.php', 'w', encoding='utf-8') as f:
    f.write(header_php_content)

print("Created includes/header.php")

# Footer extraction
footer_start = index_raw.find('<footer')
footer_end = index_raw.find('</footer>') + len('</footer>')
footer_html = index_raw[footer_start:footer_end]
footer_html = replace_links_and_assets(footer_html)

footer_php_content = footer_html + """

    <!-- Jquery Library File -->
    <script src="assets/js/jquery-3.7.1.min.js"></script>
    <!-- Bootstrap js file -->
    <script src="assets/js/bootstrap.min.js"></script>
    <!-- Validator js file -->
    <script src="assets/js/validator.min.js"></script>
    <!-- SlickNav js file -->
    <script src="assets/js/jquery.slicknav.js"></script>
    <!-- Swiper js file -->
    <script src="assets/js/swiper-bundle.min.js"></script>
    <!-- Counter js file -->
    <script src="assets/js/jquery.waypoints.min.js"></script>
    <script src="assets/js/jquery.counterup.min.js"></script>
    <!-- Magnific js file -->
    <script src="assets/js/jquery.magnific-popup.min.js"></script>
    <!-- SmoothScroll -->
    <script src="assets/js/SmoothScroll.js"></script>
    <!-- Parallax js -->
    <script src="assets/js/parallaxie.js"></script>
    <!-- MagicCursor js file -->
    <script src="assets/js/gsap.min.js"></script>
    <script src="assets/js/magiccursor.js"></script>
    <!-- Text Effect js file -->
    <script src="assets/js/splitType.js"></script>
    <script src="assets/js/ScrollTrigger.min.js"></script>
    <!-- YTPlayer js file -->
    <script src="assets/js/jquery.mb.YTPlayer.min.js"></script>
    <!-- Wow js file -->
    <script src="assets/js/wow.js"></script>
    <!-- Main Custom js file -->
    <script src="assets/js/function.js"></script>
</body>
</html>
"""

with open('includes/footer.php', 'w', encoding='utf-8') as f:
    f.write(footer_php_content)

print("Created includes/footer.php")

# Pages configuration
pages_info = [
    ('index', 'index.php', 'home', 'Intellect Homes | Custom Builder Victoria'),
    ('about-us', 'about-us.php', 'about', 'About Us | Intellect Homes'),
    ('home-designs', 'home-designs.php', 'designs', 'Home Designs | Intellect Homes'),
    ('facades', 'facades.php', 'facades', 'Facades | Intellect Homes'),
    ('floor-plan', 'floor-plan.php', 'floor-plan', 'Floor Plans | Intellect Homes'),
    ('gallery', 'gallery.php', 'gallery', 'Gallery | Intellect Homes'),
    ('blogs', 'blogs.php', 'blogs', 'Blogs & Insights | Intellect Homes'),
    ('contact-us', 'contact-us.php', 'contact', 'Contact Us | Intellect Homes'),
    ('thank-you', 'thank-you.php', 'thank-you', 'Thank You | Intellect Homes')
]

for raw_name, out_file, page_key, title in pages_info:
    raw_path = f'raw_pages/{raw_name}.html'
    if not os.path.exists(raw_path):
        continue
    with open(raw_path, 'r', encoding='utf-8') as f:
        page_html = f.read()

    # Extract body content between </header> and <footer
    h_end = page_html.find('</header>')
    if h_end != -1:
        h_end += len('</header>')
    else:
        h_end = 0

    f_start = page_html.find('<footer')
    if f_start == -1:
        f_start = len(page_html)

    body_content = page_html[h_end:f_start].strip()
    body_content = replace_links_and_assets(body_content)

    php_code = f"""<?php
$page_title = "{title}";
$current_page = "{page_key}";
require_once __DIR__ . '/includes/header.php';
?>

{body_content}

<?php
require_once __DIR__ . '/includes/footer.php';
?>
"""
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(php_code)
    print(f"Created {out_file} ({len(php_code)} bytes)")

print("\nAll PHP pages converted successfully!")
