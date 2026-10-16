import html,re,glob
E=html.escape
NV="Not yet verified — check owner's manual"
PEND="Not yet verified — source pending"
SV={k:open(f'assets/icon-{k}.svg').read().strip() for k in ['copy','print','menu','chevron','warning','arrow','swipe']}
def I(k): return SV[k].replace('<svg ',f'<svg class="i" aria-hidden="true" ',1)
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">'
TOP=f'''<header class="topbar"><div class="topbar__in"><a class="brand" href="index.html"><img src="assets/logo.svg" alt=""><span>CarSpec<b>Fix</b></span></a><nav class="topnav" aria-label="Main"><a href="index.html">Specs</a><a href="#">Symptoms</a><a href="#">Trouble codes</a><a href="#">Maintenance</a></nav><form class="quick" action="code-p0455.html" role="search"><input aria-label="Search" placeholder="Code (P0455) or vehicle (2020 RAV4)"><button>Go</button></form><button class="menu" aria-label="Menu">{I("menu")}</button></div></header>'''
FOOT='''<footer class="foot"><div class="foot__in"><span>CarSpecFix — data from owner's manuals, NHTSA, fueleconomy.gov and RepairPal. Every figure cites its source.</span><nav><a href="#">Data sources</a><a href="#">About</a><a href="#">Privacy</a><a href="#">Contact</a></nav></div></footer>'''
JS='''<script>document.addEventListener('click',e=>{const c=e.target.closest('[data-copy]');if(c){let t=c.dataset.copy;if(!t){const s=c.closest('section');t=s?s.innerText:''}navigator.clipboard&&navigator.clipboard.writeText(t);const l=c.querySelector('span');if(l){l.textContent='Copied';setTimeout(()=>l.textContent='Copy',1200)}}if(e.target.closest('[data-print]'))window.print()})</script>'''
def page(t,body,desc=''):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(t)}</title><meta name="description" content="{E(desc)}">{FONTS}<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="components.css"></head><body>{TOP}<main class="wrap">{body}</main>{FOOT}{JS}</body></html>'
def crumbs(*p):
    out=[]
    for i,(t,h) in enumerate(p):
        out.append(f'<a href="{h}">{E(t)}</a>' if h else f'<span aria-current="page">{E(t)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">'+'<span class="sep">›</span>'.join(out)+'</nav>'
COPY=lambda d='':f'<button class="btn" data-copy="{E(d)}">{I("copy")}<span>Copy</span></button>'
PRINT=f'<button class="btn btn-print" data-print>{I("print")}<span>Print</span></button>'
def sev(l): return {'Low':'<span class="sev sev--low">Low</span>','Medium':'<span class="sev sev--med">Medium</span>','High':'<span class="sev sev--high">High</span>'}.get(l,'<span class="sev sev--na">Not rated</span>')
def ref(n): return f'<sup class="ref"><a href="#ref-{n}">[{n}]</a></sup>'
def sec(label,body,tools=True,id=''):
    t=f'<div class="btns">{COPY()}{PRINT}</div>' if tools else ''
    return f'<section class="sec"{f" id={chr(34)}{id}{chr(34)}" if id else ""}><div class="sec__h"><h2 class="label">{label}</h2>{t}</div><div class="sec__body">{body}</div></section>'
def kv(rows):
    o='<table class="kv"><tbody>'
    for r in rows:
        k=r[0]
        if len(r)>1 and r[1]:
            _,n,u,src,rn=r
            o+=f'<tr><th scope="row">{E(k)}</th><td><button class="btn kv-copy" data-copy="{E(n+" "+u)}" aria-label="Copy {E(k)}">{I("copy")}</button><span class="fig mono">{E(n)}<small>{E(u)}</small></span>{ref(rn)}<span class="src">Source [{rn}]: {src}</span></td></tr>'
        else:
            o+=f'<tr><th scope="row">{E(k)}</th><td><span class="nv">{NV}</span><span class="src">Source: none yet</span></td></tr>'
    return o+'</tbody></table>'
def dt(head,rows,numcols=(),codecols=(),note=''):
    th=''.join(f'<th scope="col"{" class=num" if i in numcols else ""}>{E(h)}</th>' for i,h in enumerate(head))
    tb=''
    for r in rows:
        tb+='<tr>'+''.join((f'<td><span class="nv">{E(c)}</span></td>' if c.startswith('Not yet') else f'<td{" class=num" if i in numcols else (" class=code" if i in codecols else "")}>{c}</td>') for i,c in enumerate(r))+'</tr>'
    return f'<div class="scroll" role="region" tabindex="0" aria-label="table"><table class="dt"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div><div class="swipe">{I("swipe")} Scroll table sideways</div>'+(f'<p class="tnote">{note}</p>' if note else '')
AD=lambda k='below':f'<div class="ad ad--{k}" aria-label="Advertisement">{"300 × 250" if k=="side" else "728 × 90 / 320 × 100"}</div>'
def refs(items):
    return sec('Sources','<ol class="refs">'+''.join(f'<li id="ref-{i+1}">{x}</li>' for i,x in enumerate(items))+'</ol>',tools=False,id='sources')
def box(h,b): return f'<div class="box"><div class="box__h">{h}</div><div class="box__b">{b}</div></div>'

# ---------- HOME
years=''.join(f'<option{" selected" if y==2020 else ""}>{y}</option>' for y in range(2025,2014,-1))
makes=[("Acura",0),("Audi",0),("BMW",0),("Buick",0),("Cadillac",0),("Chevrolet",0),("Chrysler",0),("Dodge",0),("Ford",0),("GMC",0),("Honda",0),("Hyundai",0),("Jeep",0),("Kia",0),("Lexus",0),("Mazda",0),("Nissan",0),("Ram",0),("Subaru",0),("Tesla",0),("Toyota",1),("Volkswagen",0),("Volvo",0)]
mk=''.join(f'<li><a href="spec-2020-rav4.html">{m}</a><span class="ct">{n} model</span></li>' if n else f'<li><span class="off">{m}</span><span class="ct">soon</span></li>' for m,n in makes)
home=crumbs(("Home",None))+f'''<h1 class="title">Car specs by year, make &amp; model</h1><p class="sub">Oil capacity, tire pressure, fuses, recalls, symptoms and trouble codes. Every figure cites its source.</p>
<div class="main" style="margin-top:12px">
<form class="lookup" action="spec-2020-rav4.html"><div class="lookup__row"><label>Year<select>{years}</select></label><label>Make<select><option selected>Toyota</option><option>Honda</option><option>Ford</option><option>Chevrolet</option><option>Nissan</option></select></label><label>Model<select><option>RAV4</option></select></label><div class="go"><button class="btn btn--accent" type="submit">Show specs</button></div></div></form>
<div class="cols">
{sec("Look up a trouble code",'<form class="lookup" style="border-top-width:1px;background:#fff" action="code-p0455.html"><div class="lookup__row" style="grid-template-columns:1fr auto"><label>OBD-II code<input class="mono" placeholder="P0455"></label><div class="go" style="grid-column:auto"><button class="btn btn--primary" type="submit">Check code</button></div></div></form>',tools=False)}
{sec("Symptoms",'<ul class="list"><li><a href="symptom-brakes-squeaking.html">Brakes squeaking</a>'+sev("na")+'</li><li><span>Car shakes when braking</span><span class="sev sev--na">Soon</span></li><li><span>Grinding noise when braking</span><span class="sev sev--na">Soon</span></li><li><span>Check engine light</span><span class="sev sev--na">Soon</span></li></ul>',tools=False)}
</div>
{sec("Browse by make",'<ul class="makes">'+mk+'</ul>',tools=False)}
{sec("Vehicles with published specs",dt(["Year","Make","Model","Pages","Status"],[["2020","Toyota",'<a href="spec-2020-rav4.html">RAV4</a>',"Specs · Recalls · MPG","Published"],["2018","Toyota","Camry","—","Coming soon"],["2019","Honda","CR-V","—","Coming soon"],["2017","Ford","F-150","—","Coming soon"]],numcols=(),codecols=(0,)),tools=False)}
</div>'''
open('index.html','w').write(page("Car Specs by Year, Make & Model – Oil, Tires, Fuses & Fixes | CarSpecFix",home))

# ---------- SPEC
OM="Toyota owner's manual OM0R024U (model year to be confirmed)"
spec_rows=[("Oil capacity, with filter","4.8","qt / 4.5 L",'owner\'s manual, p.666',1),("Oil viscosity","SAE 0W-16","(0W-20 acceptable)","owner's manual, p.667",1),("Tire size, 17-in type A","225/65R17","102H","owner's manual, p.671",1),("Tire pressure, type A (cold)","35","psi / 241 kPa / 2.4 bar","owner's manual, p.671 · metric converted",1),("Wiper blade sizes",),("Battery group size",),("Fuse box diagram",),("Towing capacity",)]
fe=dt(["Model","Engine / transmission","Drive","City","Hwy","Comb."],[["RAV4","Auto (S8), 4 cyl, 2.5 L, SIDI &amp; PFI","FWD","27","35","30"],["RAV4","Auto (S8), 4 cyl, 2.5 L, SIDI &amp; PFI; Stop-Start","FWD","28","35","30"],["RAV4 AWD","Auto (S8), 4 cyl, 2.5 L, SIDI &amp; PFI","AWD","25","33","28"],["RAV4 AWD","Auto (S8), 4 cyl, 2.5 L, SIDI &amp; PFI; Stop-Start","AWD","27","33","29"],["RAV4 AWD LE","Auto (S8), 4 cyl, 2.5 L","AWD","27","34","30"]],numcols=(3,4,5),note=f'MPG = EPA estimates. Source {ref(2)} fueleconomy.gov, fetched 2026-10-15.')
rc=dt(["Campaign","Component","Report date"],[["20V682000","Fuel system, gasoline: delivery: fuel pump","2020-11-04"],["20V734000","Air bags: frontal","2020-11-25"],["20V064000","Engine and engine cooling","2020-02-06"],["20V373000","Steering: electric power assist system","2020-06-24"],["20V286000","Suspension: front: control arm: lower arm","2020-05-20"],["23V865000","Air bags: sensor: occupant classification","2023-12-20"]],codecols=(0,2),note=f'Source {ref(3)} NHTSA recalls database, fetched 2026-10-15. Check your VIN at nhtsa.gov/recalls.')
probs='<ul class="list"><li><a href="symptom-brakes-squeaking.html">Brakes squeaking</a>'+sev('na')+'</li><li><a href="code-p0455.html">P0455 – EVAP large leak</a>'+sev('na')+'</li></ul>'
spec=crumbs(("Home","index.html"),("Specs","index.html"),("Toyota","index.html"),("RAV4","#"),("2020",None))+f'''<h1 class="title">2020 Toyota RAV4 specs: oil, tires, fuses &amp; recalls</h1>
<div class="toolbar"><span class="grow">Updated <span class="mono">2026-10-15</span> · 4 of 8 specs verified · <a href="#sources">3 sources</a></span><button class="btn" data-print>{I("print")}<span>Print page</span></button></div>
<div class="grid"><div class="main">
<div class="notice" role="note">{I("warning")}<span>The model year of manual OM0R024U is not yet confirmed. Check your own owner's manual before relying on these values.</span></div>
{sec("Specifications",kv(spec_rows),id="specs")}
{sec("Fuel economy (mpg)",fe,id="mpg")}
{AD()}
{sec("Recalls (6)",rc,id="recalls")}
{AD()}
<div class="m-only" style="display:flex;flex-direction:column;gap:16px">{sec("Common problems",probs,tools=False)}{sec("TPMS reset",f'<span class="nv">{NV}</span>',tools=False)}</div>
{refs([f"{OM}. Pages cited per figure.","fueleconomy.gov (U.S. EPA / DOE), 2020 Toyota RAV4, fetched 2026-10-15.","NHTSA recalls database, 2020 Toyota RAV4, fetched 2026-10-15."])}
</div><aside class="side">
{box("2020 Toyota RAV4",'<ul><li class="row"><span>Oil</span><b class="mono">4.8 qt</b></li><li class="row"><span>Viscosity</span><b class="mono">0W-16</b></li><li class="row"><span>Tire</span><b class="mono">225/65R17</b></li><li class="row"><span>Pressure</span><b class="mono">35 psi</b></li><li class="row"><span>Recalls</span><b class="mono">6</b></li></ul>')}
{box("On this page",'<ul><li><a href="#specs">Specifications</a></li><li><a href="#mpg">Fuel economy</a></li><li><a href="#recalls">Recalls</a></li><li><a href="#sources">Sources</a></li></ul>')}
{box("Common problems",probs)}
{box("TPMS reset",f'<span class="nv">{NV}</span>')}
{AD("side")}
</aside></div>'''
open('spec-2020-rav4.html','w').write(page("2020 Toyota RAV4 Specs: Oil Capacity, Tire Pressure, Fuses & Recalls | CarSpecFix",spec))

# ---------- ISSUE pages
def issue(cr,title,code,defn,drive,rows,srcs,costnote):
    sevtbl=f'<table class="kv"><tbody><tr><th scope="row">Severity</th><td>{sev("na")} <span class="src" style="display:inline;margin-left:6px">Scale: {sev("Low")} {sev("Medium")} {sev("High")}</span></td></tr>'
    if defn: sevtbl+=f'<tr><th scope="row">Definition (SAE J2012, generic)</th><td><b>{defn}</b><span class="src">Source: citable public source not yet attached</span></td></tr>'
    sevtbl+=f'<tr><th scope="row">Possible causes</th><td><span class="nv">{PEND}</span></td></tr><tr><th scope="row">Can I still drive?</th><td><span class="nv">{PEND}</span>'+(f'<span class="src" style="color:var(--ink-2)">{drive}</span>' if drive else '')+'</td></tr></tbody></table>'
    aff='<ul class="list"><li><a href="spec-2020-rav4.html">2020 Toyota RAV4 specs</a><span class="ct mono" style="font-size:11px;color:var(--ink-3)">1 vehicle</span></li></ul>'
    return crumbs(*cr)+f'''<h1 class="title">{title}</h1>
<div class="toolbar"><span class="grow">{"Code <b class=mono>"+code+"</b> · " if code else ""}Severity {sev("na")} · <a href="#sources">Sources</a></span><button class="btn" data-copy="">{I("copy")}<span>Copy</span></button><button class="btn" data-print>{I("print")}<span>Print</span></button></div>
<div class="grid"><div class="main">
{sec("Summary",sevtbl,tools=False)}
{sec("Repair cost (US national average)",dt(["Repair","Range (USD)","Source"],rows,numcols=(1,),note=costnote))}
{AD()}
<div class="m-only" style="display:flex;flex-direction:column">{sec("Affected vehicles",aff,tools=False)}</div>
{refs(srcs)}
</div><aside class="side">{box("Affected vehicles",aff)}{box("Look up a code",'<form class="quick" style="width:100%" action="code-p0455.html"><input placeholder="P0455" aria-label="Code"><button>Go</button></form>')}{AD("side")}</aside></div>'''
RPn=lambda:f'RepairPal {ref(1)}'
open('symptom-brakes-squeaking.html','w').write(page("Brakes Squeaking: Causes, Can You Drive & Repair Cost | CarSpecFix",issue([("Home","index.html"),("Symptoms","#"),("Brakes squeaking",None)],"Brakes squeaking: causes, can you drive &amp; repair cost",None,None,"Brake issues: have it inspected promptly.",[["Brake pad replacement","$335–$394",RPn()],["Brake rotor replacement","$574–$698",RPn()]],["RepairPal Fair Price Estimator, national average excl. tax and location, last updated 2026-09-03."],"Estimates exclude tax and local labor rates.")))
open('code-p0455.html','w').write(page("P0455 Code: Meaning, Causes & Repair Cost | CarSpecFix",issue([("Home","index.html"),("Trouble codes","#"),("P0455",None)],"P0455: meaning, causes &amp; repair cost","P0455","Evaporative Emission System Leak Detected (large leak)",None,[["EVAP purge valve replacement",NV,NV],["Gas cap replacement",NV,NV]],["Repair cost source pending: no figures published until a citable source is attached."],"")))

# ---------- GALLERY
g=crumbs(("Home","index.html"),("Components",None))+f'''<h1 class="title">Component reference</h1><p class="sub">All components from components.css. Mobile behaviour applies below 1024px.</p><div class="main" style="margin-top:12px">
{sec("Buttons",f'<div class="btns" style="flex-wrap:wrap;gap:8px"><button class="btn btn--accent">Show specs</button><button class="btn btn--primary">Check code</button>{COPY()}<button class="btn" data-print>{I("print")}<span>Print</span></button></div>',tools=False)}
{sec("Severity tags",f'{sev("Low")} {sev("Medium")} {sev("High")} {sev("na")}',tools=False)}
{sec("Spec sheet (figure + source)",kv(spec_rows[:2]+[spec_rows[4]]))}
{sec("Data table (scrolls sideways below 1024px)",rc)}
{sec("Data table, forced 358px (mobile preview)",f'<div style="max-width:358px">{fe.replace("class=\"dt\"","class=\"dt\" style=\"min-width:620px\"")}</div>')}
{sec("Notice",f'<div class="notice">{I("warning")}<span>The model year of manual OM0R024U is not yet confirmed.</span></div>',tools=False)}
{sec("Ad slots (below tables / sidebar only)",AD()+'<div style="height:8px"></div>'+AD("side"),tools=False)}
{sec("Side box (infobox)",'<div style="max-width:300px">'+box("2020 Toyota RAV4",'<ul><li class="row"><span>Oil</span><b class="mono">4.8 qt</b></li><li class="row"><span>Pressure</span><b class="mono">35 psi</b></li></ul>')+'</div>',tools=False)}
{sec("Source references",'<p>Figure with reference'+ref(1)+'</p>'+'<ol class="refs" style="margin-top:6px"><li>Toyota owner\'s manual OM0R024U, p.666.</li></ol>',tools=False)}
{sec("Header / footer",'<p class="sub">Shown at the top and bottom of this page. The navigation collapses to a menu button below 1024px.</p>',tools=False)}
{sec("Icons &amp; logo (assets/)",' '.join(f'<span class="btn">{I(k)}{k}</span>' for k in SV)+' <span class="btn"><img src="assets/logo.svg" width="14" height="14" alt="">logo</span>',tools=False)}
</div>'''
open('components.html','w').write(page("Components | CarSpecFix",g))
