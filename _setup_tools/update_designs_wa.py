import re
import urllib.parse

with open('designs.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(
    r"(openPlanDetails\('([^']+)'[^\n]*\)\">\s*View Plan &amp; Specs\s*</button>\s*)<button class=\"btn btn-primary\" data-open-modal=\"consultModal\">Enquire</button>",
    re.DOTALL
)

def repl(m):
    prefix = m.group(1)
    title = m.group(2)
    msg = f"Hi Intellect Homes, I would like to enquire about {title}."
    wa_url = f"https://wa.me/61411560177?text={urllib.parse.quote(msg)}"
    return f'{prefix}<a href="{wa_url}" target="_blank" rel="noopener" class="btn btn-primary">Enquire</a>'

new_html, count = pattern.subn(repl, html)
with open('designs.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print(f"Updated {count} Enquire buttons to WhatsApp links.")
