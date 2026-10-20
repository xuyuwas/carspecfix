import re, html, subprocess, sys

def get(u):
    return subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout

def flat(t):
    t = re.sub(r'<svg.*?</svg>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' | ', t)
    return re.sub(r'(\s*\|\s*)+', ' | ', html.unescape(t)).strip()

def oil_card(t):
    i = t.find('<div class="oil">')
    if i < 0:
        return '(no oil card)'
    seg = t[i:i + 1500]
    j = seg.find('</div></div>')
    return flat(seg[:j + 12])[:420]

def meta(t):
    ti = re.search(r'<title>(.*?)</title>', t)
    de = re.search(r'name="description" content="(.*?)"', t)
    h1 = re.search(r'<h1.*?</h1>', t, re.S)
    return (ti.group(1) if ti else '?', de.group(1) if de else '?', flat(h1.group(0)) if h1 else '?')

pages = {
    'RAV4 2024': 'https://carspecfix.com/specs/toyota/rav4/2024/',
    'RAV4 2010': 'https://carspecfix.com/specs/toyota/rav4/2010/',
    'Camry 2022': 'https://carspecfix.com/specs/toyota/camry/2022/',
    'RAV4 2020': 'https://carspecfix.com/specs/toyota/rav4/2020/',
    'CR-V 2024': 'https://carspecfix.com/specs/honda/cr-v/2024/',
    'Equinox 2022': 'https://carspecfix.com/specs/chevrolet/equinox/2022/',
    'Accord 2022': 'https://carspecfix.com/specs/honda/accord/2022/',
}
for name, u in pages.items():
    t = get(u)
    title, desc, h1 = meta(t)
    print('###', name)
    print('  TITLE', len(title), '|', title)
    print('  DESC ', len(desc), '|', desc[:150])
    print('  H1   ', h1[:90])
    print('  OIL  ', oil_card(t))
    print('  flags', 'null' if 'null' in t else '-', '| NaN' if 'NaN' in t else '-')
    print()

hub = get('https://carspecfix.com/specs/toyota/rav4/')
print('### RAV4 hub')
print('  chips', len(re.findall(r'href="/specs/toyota/rav4/\d{4}/"', hub)), '| powertrain note:', 'Powertrains' in hub)
i = hub.find('Powertrains')
if i > 0:
    print('  ', flat(hub[i:i + 400])[:260])
