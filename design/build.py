import html
E=html.escape
NV="Not yet verified — check owner's manual"
PEND="Not yet verified — source pending"
def head(title,desc=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="components.css"></head><body>'''
HEADER='''<header class="site-header"><div class="site-header__in"><a class="logo" href="index.html"><img src="assets/logo.svg" width="28" height="28" alt=""><span>CarSpec<b>Fix</b></span></a><nav class="nav" aria-label="Main"><a href="#">Specs</a><a href="#">Symptoms</a><a href="#">Codes</a><a href="#">Maintenance</a></nav><button class="menu-btn" aria-label="Menu"><span class="i i-menu"></span></button></div></header>'''
FOOTER='''<footer class="site-footer"><div class="site-footer__in"><p style="margin:0">Data from owner's manuals, NHTSA, fueleconomy.gov and RepairPal — every number cites its source.</p><nav><a href="#">Data sources</a><a href="#">About</a><a href="#">Privacy</a><a href="#">Contact</a></nav></div></div></footer>'''.replace('</div></div></footer>','</div></footer>')
SCRIPT='''<script>document.addEventListener('click',e=>{const c=e.target.closest('[data-copy]');if(c){const t=c.dataset.copy||c.closest('[data-copy-scope]')?.innerText||'';navigator.clipboard&&navigator.clipboard.writeText(t);c.lastChild.textContent=' Copied';setTimeout(()=>c.lastChild.textContent=' Copy',1200)}if(e.target.closest('[data-print]'))window.print()})</script>'''
def page(title,desc,body):
    return head(title,desc)+HEADER+'<main class="container">'+body+'</main>'+FOOTER+SCRIPT+'</body></html>'
def btn(kind,icon,label,attrs=""):
    ic=f'<span class="i i-{icon}"></span>' if icon else ''
    return f'<button class="btn btn--{kind}" {attrs}>{ic}<span>{label}</span></button>' if icon else f'<button class="btn btn--{kind}" {attrs}>{label}</button>'
def copybtn(): return '<button class="btn btn--secondary" data-copy><span class="i i-copy"></span><span> Copy</span></button>'
def printbtn(): return '<button class="btn btn--secondary btn-print" data-print><span class="i i-print"></span><span> Print</span></button>'
def sev(l): return f'<span class="sev sev--{l.lower() if l!="Not yet rated" else "unrated"}">{l}</span>'
def num(label,n=None,sub=None,src=None):
    if n:
        val=f'<div class="num__value"><span class="num__n">{E(n)}</span>'+(f'<span class="num__sub">{E(sub)}</span>' if sub else '')+'</div>'
        s=f'<a href="#">{E(src)}</a>'
        cp=f'{n} {sub or ""}'.strip()
    else:
        val=f'<div class="unverified">{NV}</div>'; s='—'; cp=NV
    return f'<div class="num"><div class="num__top"><span class="num__label">{E(label)}</span><button class="copy-link" data-copy="{E(cp)}"><span class="i i-copy"></span><span> Copy</span></button></div>{val}<div class="num__src"><span class="src-label">SOURCE</span><span>{s}</span></div></div>'
def table(title,headcols,rows,source,numcols=()):
    th=''.join(f'<th scope="col">{E(h)}</th>' for h in headcols)
    tr=''
    for r in rows:
        tds=''
        for i,c in enumerate(r):
            cls=' class="n"' if i in numcols and not c.startswith('Not yet') else ''
            inner=f'<span class="unverified">{E(c)}</span>' if c.startswith('Not yet') else E(c)
            tds+=f'<td{cls}>{inner}</td>'
        tr+=f'<tr>{tds}</tr>'
    return f'''<section class="spec-table" data-copy-scope><div class="spec-table__head"><h2 class="h2">{E(title)}</h2><div class="spec-table__actions">{copybtn()}{printbtn()}</div></div><div class="spec-table__scroll" tabindex="0" role="region" aria-label="{E(title)} table"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div><div class="swipe-hint"><span class="i i-swipe"></span>Swipe to see all columns</div><p class="source-line">{source}</p></section>'''
def ad(kind='below'):
    return f'<div class="ad ad--{kind}" aria-label="Advertisement"><b>ADVERTISEMENT</b><span>{"300×250 · sidebar" if kind=="sidebar" else "728×90 desktop / 320×100 mobile · below table"}</span></div>'
arrow='<span class="i i-arrow"></span>'
def link(t,href='#'): return f'<a class="link" href="{href}">{E(t)}{arrow}</a>'

# HOME
def sel(l,opts,cur):
    o=''.join(f'<option{" selected" if x==cur else ""}>{x}</option>' for x in opts)
    return f'<label class="field">{l}<span class="select"><select>{o}</select><span class="i i-chevron"></span></span></label>'
home=f'''<div class="main"><nav class="crumbs" aria-label="Breadcrumb"><span>Home</span></nav>
<section class="hero"><h1>Car Specs by Year, Make &amp; Model</h1><p>Oil capacity, tire pressure, fuses, recalls — plus what your warning light or noise means.</p>
<form class="lookup" action="spec-2020-rav4.html">{sel("Year",[str(y) for y in range(2025,2014,-1)],"2020")}{sel("Make",["Toyota","Honda","Ford","Chevrolet","Nissan"],"Toyota")}{sel("Model",["RAV4"],"RAV4")}<button class="btn btn--accent btn--block" type="submit">Show specs</button></form></section>
<div class="two"><section class="card"><h2 class="h2">Look up a trouble code</h2><form class="code-form" action="code-p0455.html"><input class="input" placeholder="e.g. P0455" aria-label="Trouble code"><button class="btn btn--primary" type="submit">Check code</button></form></section>
<section class="card"><h2 class="h2">What's wrong with my car?</h2><div class="chips"><a class="chip" href="symptom-brakes-squeaking.html">Brakes squeaking{arrow}</a><span class="chip">Car shakes when braking</span><span class="chip">Grinding noise when braking</span><span class="chip">Check engine light</span></div></section></div>
<section style="display:flex;flex-direction:column;gap:12px"><h2 class="h2">Popular vehicles</h2><div class="vehicles"><a class="vehicle vehicle--active" href="spec-2020-rav4.html"><strong>2020 Toyota RAV4</strong><span>Oil · Tires · Recalls{arrow}</span></a>'''+''.join(f'<div class="vehicle"><strong>{v}</strong><span>Coming soon</span></div>' for v in ["2018 Toyota Camry","2019 Honda CR-V","2017 Ford F-150"])+'</div></section></div>'
open('index.html','w').write(page("Car Specs by Year, Make & Model – Oil, Tires, Fuses & Fixes | CarSpecFix","Oil capacity, tire pressure, fuses, recalls — plus what your warning light or noise means.",home))

# SPEC
M="Toyota owner's manual OM0R024U (model year to be confirmed)"
nums=''.join([num("Oil capacity (with filter)","4.8 qt","/ 4.5 L",M+", p.666"),num("Oil viscosity","SAE 0W-16","(0W-20 acceptable)",M+", p.667"),num("Tire size (17-in type A)","225/65R17","102H",M+", p.671"),num("Tire pressure (type A)","35 psi","/ 241 kPa / 2.4 bar",M+", p.671 · metric converted"),num("Wiper blade sizes"),num("Battery group size"),num("Fuse box diagram"),num("Towing capacity")])
fe=table("Fuel economy (city / hwy / combined mpg)",["Model","Engine / trans","Drive","MPG"],[["RAV4","Auto (S8), 4 cyl, 2.5 L, SIDI & PFI","Front-Wheel Drive","27/35/30"],["RAV4","Auto (S8), 4 cyl, 2.5 L, SIDI & PFI; Stop-Start","Front-Wheel Drive","28/35/30"],["RAV4 AWD","Auto (S8), 4 cyl, 2.5 L, SIDI & PFI","All-Wheel Drive","25/33/28"],["RAV4 AWD","Auto (S8), 4 cyl, 2.5 L, SIDI & PFI; Stop-Start","All-Wheel Drive","27/33/29"],["RAV4 AWD LE","Auto (S8), 4 cyl, 2.5 L","All-Wheel Drive","27/34/30"]],'Source: <a href="#">fueleconomy.gov (EPA)</a>, fetched 2026-10-15',(3,))
rc=table("Recalls (6)",["NHTSA campaign","Component","Date"],[["20V682000","FUEL SYSTEM, GASOLINE: DELIVERY: FUEL PUMP","2020-11-04"],["20V734000","AIR BAGS: FRONTAL","2020-11-25"],["20V064000","ENGINE AND ENGINE COOLING","2020-02-06"],["20V373000","STEERING: ELECTRIC POWER ASSIST SYSTEM","2020-06-24"],["20V286000","SUSPENSION: FRONT: CONTROL ARM: LOWER ARM","2020-05-20"],["23V865000","AIR BAGS: SENSOR: OCCUPANT CLASSIFICATION","2023-12-20"]],'Source: <a href="#">NHTSA</a>, fetched 2026-10-15. Check your VIN at nhtsa.gov/recalls.',(2,))
probs=f'<section class="card"><h2 class="h2">Common problems</h2><div class="row-between">{link("Brakes squeaking","symptom-brakes-squeaking.html")}{sev("Not yet rated")}</div><div class="row-between">{link("P0455 – EVAP large leak","code-p0455.html")}{sev("Not yet rated")}</div></section>'
tpms=f'<section class="card"><h2 class="h2">TPMS reset</h2><div class="unverified">{NV}</div></section>'
spec=f'''<div class="layout"><div class="main"><div style="display:flex;flex-direction:column;gap:10px"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>›<a href="#">Specs</a>›<a href="#">Toyota</a>›<a href="#">RAV4</a>›<span>2020</span></nav>
<h1 class="page-title">2020 Toyota RAV4 Specs: Oil, Tires, Fuses &amp; Recalls</h1><div class="meta"><span>Updated 2026-10-15 · Every number links to its source</span><button class="btn btn--secondary" data-print><span class="i i-print"></span><span> Print page</span></button></div>
<div class="alert" role="note"><span class="i i-warning"></span><span>Manual model year is not yet confirmed. Verify against your own owner's manual before relying on these values.</span></div></div>
<section class="nums" id="key-numbers" aria-label="Key numbers">{nums}</section>
{fe}{ad()}{rc}{ad()}<div class="mobile-only" style="flex-direction:column;gap:24px">{probs}{tpms}</div></div>
<aside class="sidebar"><nav class="card toc"><strong>On this page</strong><a href="#key-numbers">Key numbers</a><a href="#">Fuel economy</a><a href="#">Recalls</a><a href="#">Common problems</a><a href="#">TPMS reset</a></nav>{probs}{tpms}{ad("sidebar")}</aside></div>'''
open('spec-2020-rav4.html','w').write(page("2020 Toyota RAV4 Specs: Oil Capacity, Tire Pressure, Fuses & Recalls | CarSpecFix","",spec))

def issue(crumb,title,defn,drive,rows,tsrc):
    blocks=''
    if defn: blocks+=f'<section class="card"><h2 class="h2">Definition (SAE J2012 generic)</h2><p style="margin:0;font-size:22px;font-weight:700;line-height:1.25">{defn}</p><div class="num__src"><span class="src-label">SOURCE</span><span class="unverified" style="font-size:12px">Citable public source: not yet attached</span></div></section>'
    blocks+=f'<section class="card"><h2 class="h2">Possible causes</h2><div class="unverified">{PEND}</div></section>'
    blocks+=f'<section class="card"><h2 class="h2">Can I still drive?</h2><div class="unverified">{PEND}</div>'+(f'<p style="margin:0;color:var(--text-secondary);font-size:13px">{drive}</p>' if drive else '')+'</section>'
    aff=f'<section class="card"><h2 class="h2">Affected vehicles</h2>{link("2020 Toyota RAV4 specs","spec-2020-rav4.html")}</section>'
    return f'''<div class="layout"><div class="main"><div style="display:flex;flex-direction:column;gap:12px"><nav class="crumbs" aria-label="Breadcrumb">{crumb}</nav><h1 class="page-title">{title}</h1><div class="meta"><button class="btn btn--secondary" data-copy=""><span class="i i-copy"></span><span> Copy</span></button><button class="btn btn--secondary" data-print><span class="i i-print"></span><span> Print</span></button></div>
<div class="sev-box"><div class="sev-row"><strong style="color:var(--text-primary);font-size:13px">Severity</strong>{sev("Not yet rated")}</div><div class="sev-row">Scale: {sev("Low")}{sev("Medium")}{sev("High")}</div></div></div>
{blocks}{table("Repair cost (US national average)",["Repair","Range","Source"],rows,tsrc,(1,))}{ad()}<div class="mobile-only" style="flex-direction:column">{aff}</div></div>
<aside class="sidebar">{aff}<section class="card"><strong>Look up a trouble code</strong><form class="code-form" action="code-p0455.html"><input class="input" placeholder="e.g. P0455" aria-label="Trouble code"></form></section>{ad("sidebar")}</aside></div>'''
RP="RepairPal · estimates last updated 2026-09-03; national avg, excl. tax/location"
open('symptom-brakes-squeaking.html','w').write(page("Brakes Squeaking: Causes, Can You Drive & Repair Cost | CarSpecFix","",issue('<a href="index.html">Home</a>›<a href="#">Symptoms</a>›<span>Brakes squeaking</span>',"Brakes Squeaking: Causes, Can You Drive &amp; Repair Cost",None,"Brake issues: have it inspected promptly.",[["Brake pad replacement","$335–$394",RP],["Brake rotor replacement","$574–$698",RP]],'Source: <a href="#">RepairPal</a>, estimates last updated 2026-09-03.')))
open('code-p0455.html','w').write(page("P0455 Code: Meaning, Causes & Repair Cost | CarSpecFix","",issue('<a href="index.html">Home</a>›<a href="#">Codes</a>›<span>P0455</span>',"P0455 Code: Meaning, Causes &amp; Repair Cost","Evaporative Emission System Leak Detected (large leak)",None,[["EVAP purge valve replacement",NV,NV],["Gas cap replacement",NV,NV]],'Source: — (pending)')))

# GALLERY
g=f'''<div class="main"><h1 class="page-title">CarSpecFix components</h1>
<section class="card"><h2 class="h2">Buttons</h2><div class="chips">{btn("primary",None,"Check code")}{btn("accent",None,"Show specs")}{copybtn()}{printbtn().replace(" btn-print","")}</div></section>
<section class="card"><h2 class="h2">Severity tags</h2><div class="chips">{sev("Low")}{sev("Medium")}{sev("High")}{sev("Not yet rated")}</div></section>
<section class="card"><h2 class="h2">Number + source</h2><div class="nums">{num("Oil capacity (with filter)","4.8 qt","/ 4.5 L",M+", p.666")}{num("Battery group size")}</div></section>
<section class="card"><h2 class="h2">Spec table (desktop / auto mobile scroll)</h2>{rc}</section>
<section class="card"><h2 class="h2">Spec table — forced mobile width (390px)</h2><div style="max-width:358px">{fe.replace('class="spec-table"','class="spec-table spec-table--mobile"')}</div><p class="source-line">Below 1024px the table keeps min-width 640px and scrolls horizontally; swipe hint shows.</p></section>
<section class="card"><h2 class="h2">Alert</h2><div class="alert"><span class="i i-warning"></span><span>Manual model year is not yet confirmed.</span></div></section>
<section class="card"><h2 class="h2">Ad slots (only below tables and in sidebar)</h2>{ad()}{ad("sidebar")}</section>
<section class="card"><h2 class="h2">Header &amp; footer</h2><p class="source-line">Shown at top and bottom of this page. Header collapses nav to a menu button below 1024px.</p></section>
<section class="card"><h2 class="h2">Icons &amp; logo (assets/*.svg)</h2><div class="chips">'''+''.join(f'<span class="chip"><span class="i i-{k}"></span>{k}</span>' for k in ["copy","print","menu","chevron","warning","arrow","swipe"])+'<span class="chip"><img src="assets/logo.svg" width="20" height="20" alt="">logo</span></div></section></div>'
open('components.html','w').write(page("Components | CarSpecFix",'',g))

# inline SVG icons (CSS mask-image is blocked on file:// and inline SVG avoids extra requests)
import re,glob
SV={k:open(f'assets/icon-{k}.svg').read().strip() for k in ['copy','print','menu','chevron','warning','arrow','swipe']}
def inl(m):
    k=m.group(1);s=SV[k]
    return s.replace('<svg ',f'<svg class="i i-{k}" aria-hidden="true" ',1)
for f in glob.glob('*.html'):
    t=open(f).read();t=re.sub(r'<span class="i i-(\w+)"></span>',inl,t);open(f,'w').write(t)
