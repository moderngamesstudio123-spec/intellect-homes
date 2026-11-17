import urllib.request
import json

for strat in ['mobile', 'desktop']:
    api = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://intellect-homes.vercel.app/&strategy={strat}&category=performance&category=accessibility&category=best-practices&category=seo'
    print(f'Running PageSpeed ({strat})...')
    try:
        with urllib.request.urlopen(api, timeout=90) as r:
            data = json.loads(r.read().decode())
        cats = data['lighthouseResult']['categories']
        audits = data['lighthouseResult']['audits']
        print(f'=== {strat.upper()} ===')
        for k, v in cats.items():
            title = v['title']
            score = int(v['score'] * 100)
            print(f'  {title}: {score}/100')
        for m in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index']:
            if m in audits:
                t = audits[m]['title']
                val = audits[m].get('displayValue', 'N/A')
                print(f'  {t}: {val}')
    except Exception as e:
        print(strat, 'Error:', e)
