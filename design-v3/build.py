import html
E=html.escape
NV="Not yet verified — check owner's manual"
PEND="Not yet verified — source pending"
SV={k:open(f'assets/icon-{k}.svg').read().strip() for k in ['copy','print','menu','chevron','warning','arrow','swipe','search']}
def I(k): return SV[k].replace('<svg ','<svg class="i" aria-hidden="true" ',1)
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">'
def HDR(cur):
    nav=''.join(f'<a href="{h}"{" aria-current=page" if t==cur else ""}>{t}</a>' for t,h in [("Specs","spec-2020-rav4.html"),("Symptoms","symptom-brakes-squeaking.html"),("Trouble codes","code-p0455.html"),("Maintenance","#")])
    return f'<header class="hdr"><div class="container hdr__in"><a class="brand" href="index.html"><img src="assets/logo.svg" width="28" height="28" alt=""><span>CarSpec<b>Fix</b></span></a><nav class="nav" aria-label="Main">{nav}</nav><form class="search" role="search" action="code-p0455.html">{I("search")}<input placeholder="Search a vehicle or code, e.g. P0455" aria-label="Search"></form><div class="hdr__icons"><button class="icon-btn" aria-label="Search">{I("search")}</button><button class="icon-btn" aria-label="Menu">{I("menu")}</button></div></div></header>'
FTR='<footer class="ftr"><div class="container ftr__in"><a class="brand" href="index.html"><img src="assets/logo.svg" width="24" height="24" alt=""><span>CarSpec<b>Fix</b></span></a><span>Data from owner\'s manuals, NHTSA and fueleconomy.gov. Every figure cites its source.</span><nav><a href="#">Data sources</a><a href="#">About</a><a href="#">Privacy</a><a href="#">Contact</a></nav></div></footer>'
JS=r"""<div class="sr-only" aria-live="polite" id="live" style="position:absolute;left:-9999px"></div><script>
(function(){
  function fallbackCopy(t){var ta=document.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();var ok=false;try{ok=document.execCommand('copy')}catch(e){ok=false}document.body.removeChild(ta);return ok}
  function copyText(t){if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t).then(function(){return true},function(){return fallbackCopy(t)})}return Promise.resolve(fallbackCopy(t))}
  function flash(btn,ok){var l=btn.querySelector('.lbl'),live=document.getElementById('live'),msg=ok?'Copied':'Copy failed';if(l){var old=l.dataset.orig||l.textContent;l.dataset.orig=old;l.textContent=msg;btn.classList.toggle('is-err',!ok);setTimeout(function(){l.textContent=old;btn.classList.remove('is-err')},1600)}else{btn.title=msg}if(live)live.textContent=msg}
  document.addEventListener('click',function(e){
    var c=e.target.closest('[data-copy]');
    if(c){var t=c.getAttribute('data-copy');if(!t){var scope=c.closest('[data-copy-scope],section');t=scope?scope.innerText.replace(/\s*(Copy|Print|Print page|Copied)\s*/g,' ').trim():document.title}copyText(t).then(function(ok){flash(c,ok)})}
    if(e.target.closest('[data-print]')){e.preventDefault();window.print()}
    var fb=e.target.closest('[data-feedback]');
    if(fb){var box=fb.closest('.feedback'),v=fb.getAttribute('data-feedback');box.querySelectorAll('[data-feedback]').forEach(function(b){b.setAttribute('aria-pressed',b===fb)});box.querySelector('.feedback__more').hidden=(v!=='no');box.querySelector('.feedback__msg').textContent=v==='yes'?'Thanks, glad it helped.':'Thanks. Tell us what was missing (optional).'}
  });
})();
</script>"""
def page(t,cur,body,desc=''):
    return f'<!doctype html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(t)}</title><meta name="description" content="{E(desc)}">{FONTS}<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="components.css"></head><body>{HDR(cur)}{body}{FTR}{JS}</body></html>'
def crumbs(*p): return '<nav class="crumbs" aria-label="Breadcrumb">'+'<span class="sep">/</span>'.join(f'<a href="{h}">{E(t)}</a>' if h else f'<span aria-current="page">{E(t)}</span>' for t,h in p)+'</nav>'
def ref(n): return f'<sup class="ref"><a href="#ref-{n}">[{n}]</a></sup>'
COPY=lambda d='':f'<button class="btn" data-copy="{E(d)}">{I("copy")}<span class="lbl">Copy</span></button>'
PRINT=f'<button class="btn btn-print" data-print>{I("print")}<span>Print</span></button>'
def tag(l): return {'Low':'<span class="tag tag--low">Low</span>','Medium':'<span class="tag tag--med">Medium</span>','High':'<span class="tag tag--high">High</span>','Example':'<span class="tag tag--example">Example</span>'}.get(l,'<span class="tag tag--na">Not rated</span>')
def section(id,title,body,kicker='',tools=True):
    t=f'<div class="tools">{COPY()}{PRINT}</div>' if tools else ''
    k=f'<p class="section__kicker">{kicker}</p>' if kicker else ''
    return f'<section id="{id}"><div class="section__head"><div><h2 class="section__title">{title}</h2>{k}</div>{t}</div>{body}</section>'
def table(cols,rows,foot,wide=False):
    th=''.join(f'<th scope="col"{" class=num" if c.startswith("#") else ""}>{E(c.lstrip("#"))}</th>' for c in cols)
    tb=''.join('<tr>'+''.join(f'<td{(" class="+chr(34)+cl+chr(34)) if cl else ""}>{v}</td>' for v,cl in r)+'</tr>' for r in rows)
    return f'<div class="tbl-wrap"><div class="tbl-scroll" role="region" tabindex="0" aria-label="table"><table class="tbl{" tbl--wide" if wide else ""}"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div><div class="tbl-foot"><span>{foot}</span><span class="swipe">{I("swipe")} Swipe for more columns</span></div></div>'
NVc=lambda: (f'<span class="nv">{NV}</span>','')
AD=lambda k='below':f'<div class="ad ad--{k}" aria-label="Advertisement"><b>ADVERTISEMENT</b><span>{"300 × 250" if k=="side" else "728 × 90 · 320 × 100 on mobile"}</span></div>'
def refs(items): return section('sources','Sources','<ol class="refs">'+''.join(f'<li id="ref-{i+1}">{x}</li>' for i,x in enumerate(items))+'</ol>',tools=False)
def feedback():
    return '<section id="feedback" class="feedback" aria-label="Feedback"><div class="feedback__row"><h2 class="feedback__q">Did this solve your problem?</h2><button class="btn" data-feedback="yes" aria-pressed="false">Yes</button><button class="btn" data-feedback="no" aria-pressed="false">No</button></div><p class="feedback__msg" role="status"></p><div class="feedback__more" hidden><label class="qa__q" for="fb-text">What was missing? (optional, no personal info)</label><textarea id="fb-text"></textarea><div><button class="btn btn--primary">Send</button></div></div><p class="report" id="report">Spotted a wrong number? <a href="#report">Report a data error</a>. Corrections are reviewed and logged.</p></section>'
def panel(t,b): return f'<div class="panel"><h3 class="panel__title">{t}</h3>{b}</div>'

# ---------- SPEC
OM="Toyota owner's manual OM0R024U (model year to be confirmed)"
ks=[("Oil capacity, with filter","4.8","qt","4.5 L · manual p.666",1),("Tire pressure, 17-in (cold)","35","psi","241 kPa · manual p.671 · metric converted",1),("Combined fuel economy","30","mpg","FWD, EPA estimate",2),("Open recall campaigns","6","","NHTSA, fetched 2026-10-15",3)]
strip='<div class="keyspecs" aria-label="Key specs">'+''.join(f'<div class="ks"><div class="ks__label">{l}</div><div class="ks__val">{v}{f"<span class=ks__unit>{u}</span>" if u else ""}{ref(n)}</div><div class="ks__src">Source [{n}] · {s}</div></div>' for l,v,u,s,n in ks)+'</div>'
TR=[("17-in","LE (FWD)","225/65R17 102H","35","35"),("17-in","LE (AWD)","225/65R17 102H","35","35"),("17-in","XLE (FWD)","225/65R17 102H","35","35"),("17-in","XLE, full load","225/65R17 102H","35","38"),("18-in","XLE Premium","225/60R18 100H","35","35"),("18-in","Adventure","225/60R18 100H","35","35"),("18-in","TRD Off-Road","225/65R18 103H","36","36"),("19-in","Limited","235/55R19 101V","35","35"),("Spare","Compact spare (all)","T165/90D18 107M","60","60")]
tires=table(["Wheel","Trim / config","Tire size","#Front psi","#Rear psi","Page","Source"],[[(w,'nowrap strong'),(f'{c} {tag("Example")}','nowrap'),(sz,'big'),(f,'num'),(r,'num'),('<span class="muted">—</span>',''),('<span class="muted">Example</span>','nowrap')] for w,c,sz,f,r in TR],
 'Pressures are cold. All 9 rows are EXAMPLE layout data (not verified). Table supports up to 10 rows; the same tire size can repeat with different psi per config.',wide=True)
def kvrow(k,fig=None,unit='',src='',n=None):
    if fig: v=f'<div class="kv__v"><span class="kv__fig">{fig}<small>{unit}</small>{ref(n)}</span><button class="copy-sm" data-copy="{E(fig+" "+unit)}" aria-label="Copy {E(k)}">{I("copy")}</button><span class="kv__src">Source [{n}] · {src}</span></div>'
    else: v=f'<div class="kv__v"><span class="nv">{NV}</span><span class="kv__src">No source yet</span></div>'
    return f'<div class="kv__row"><div class="kv__k">{k}</div>{v}</div>'
maint='<div class="kv">'+kvrow("Oil capacity, with filter","4.8","qt / 4.5 L","manual p.666",1)+kvrow("Oil viscosity","SAE 0W-16","0W-20 acceptable","manual p.667",1)+kvrow("Wiper blade sizes")+kvrow("Battery group size")+kvrow("Fuse box diagram")+kvrow("Towing capacity")+'</div>'
fe=table(["Model","Engine / transmission","Drive","#City","#Hwy","#Combined"],[[(m,'strong nowrap'),(e,''),(d,'nowrap'),(c,'num'),(h,'num'),(b,'num')] for m,e,d,c,h,b in [("RAV4","Auto (S8), 4 cyl, 2.5 L, SIDI &amp; PFI","FWD","27","35","30"),("RAV4","Auto (S8), 4 cyl, 2.5 L, SIDI &amp; PFI; Stop-Start","FWD","28","35","30"),("RAV4 AWD","Auto (S8), 4 cyl, 2.5 L, SIDI &amp; PFI","AWD","25","33","28"),("RAV4 AWD","Auto (S8), 4 cyl, 2.5 L, SIDI &amp; PFI; Stop-Start","AWD","27","33","29"),("RAV4 AWD LE","Auto (S8), 4 cyl, 2.5 L","AWD","27","34","30")]],f'Source {ref(2)} fueleconomy.gov (EPA), fetched 2026-10-15')
rc=table(["Campaign","Component","Report date"],[[(f'<span class="mono">{a}</span>','nowrap'),(b,''),(f'<span class="tnum">{c}</span>','nowrap')] for a,b,c in [("20V682000","Fuel system, gasoline: delivery: fuel pump","2020-11-04"),("20V734000","Air bags: frontal","2020-11-25"),("20V064000","Engine and engine cooling","2020-02-06"),("20V373000","Steering: electric power assist system","2020-06-24"),("20V286000","Suspension: front: control arm: lower arm","2020-05-20"),("23V865000","Air bags: sensor: occupant classification","2023-12-20")]],f'Source {ref(3)} NHTSA, fetched 2026-10-15 · Check your VIN at nhtsa.gov/recalls')
probs='<ul class="plist"><li><a href="symptom-brakes-squeaking.html">Brakes squeaking</a>'+tag('na')+'</li><li><a href="code-p0455.html">P0455 – EVAP large leak</a>'+tag('na')+'</li><li><span>TPMS reset</span><span class="nv" style="font-size:13px">Not yet verified</span></li></ul>'
years=''.join(f'<a class="chip{" chip--muted" if y!=2020 else ""}" href="#"{" aria-current=page" if y==2020 else ""}>{y}</a>' for y in (2019,2020,2021))
cfg=''.join(f'<span class="chip">{c}</span>' for c in ("FWD","AWD","AWD LE"))
qa=f'''<section class="qa" id="quick" data-copy-scope aria-label="Quick answer"><div class="qa__head"><h2 class="qa__title">Quick answer</h2><div class="tools"><button class="btn" data-copy="">{I("copy")}<span class="lbl">Copy</span></button><button class="btn" data-print>{I("print")}<span>Print</span></button></div></div>
<div class="qa__grid">
<div class="qa__item"><div class="qa__q">Engine oil</div><div class="qa__a">4.8<small>qt (4.5 L) with filter</small>{ref(1)}</div><div class="qa__more"><b>SAE 0W-16</b> (0W-20 acceptable) · 2.5 L 4-cyl</div><div class="qa__src">Manual p.666 (capacity), p.667 (viscosity) · without filter: <span class="nv" style="font-size:12px">Not yet verified</span></div></div>
<div class="qa__item"><div class="qa__q">Tire pressure (cold)</div><div class="qa__a">35<small>psi front &amp; rear</small>{ref(1)}</div><div class="qa__more">17-in type A · <b>225/65R17 102H</b>. Check the sticker on your driver's door jamb.</div><div class="qa__src">Manual p.671 · 241 kPa / 2.4 bar (metric converted) · TPMS reset: <span class="nv" style="font-size:12px">Not yet verified</span></div></div>
<div class="qa__item"><div class="qa__q">Recalls</div><div class="qa__a">6<small>NHTSA campaigns</small>{ref(3)}</div><div class="qa__more"><a href="#recalls">See campaign list</a> · check your own car by VIN at <a href="https://www.nhtsa.gov/recalls">nhtsa.gov/recalls</a></div><div class="qa__src">Fetched 2026-10-15</div></div>
</div><div class="qa__foot"><span>Last verified <span class="tnum">2026-10-15</span> · manual OM0R024U, model year to be confirmed</span><a href="#report">Report a data error</a></div></section>'''
cfg=''.join(f'<span class="chip">{c}</span>' for c in ("FWD","AWD","AWD LE"))
spec=f'''<div class="vhead vhead--compact"><div class="container">{crumbs(("Home","index.html"),("Toyota","#"),("RAV4","#"),("2020",None))}
<div class="vhead__grid" style="padding-bottom:0"><div><div class="eyebrow">Toyota · Compact SUV · 2.5 L 4-cyl</div><h1 class="vtitle"><span class="yr">2020 Toyota</span>RAV4 specs</h1></div>
<div class="vart"><img src="assets/car-suv.svg" alt="" width="360" height="135"></div></div>
{qa}
<div class="notice" role="note" style="margin-top:12px">{I("warning")}<span>The model year of manual OM0R024U is not yet confirmed. Check your own owner's manual before relying on these values.</span></div>
<div class="vmeta" style="margin:16px 0 20px"><div class="chips"><span class="vmeta__label">Year</span>{years}</div><div class="chips"><span class="vmeta__label">Config</span>{cfg}</div></div></div></div>
<nav class="subnav" aria-label="On this page"><div class="container subnav__in"><a href="#quick" aria-current="true">Quick answer</a><a href="#recalls">Recalls</a><a href="#tires">Tires</a><a href="#maintenance">Parts &amp; fluids</a><a href="#mpg">Fuel economy</a><a href="#problems">Problems</a><a href="#sources">Sources</a></div></nav>
<div class="container"><div class="layout"><div class="main">
{section("recalls","Recalls (6)",rc,kicker="Check your own vehicle by VIN at nhtsa.gov/recalls")}
{AD()}
{section("tires","Tire size &amp; pressure by configuration",tires,kicker=f'One row per wheel / configuration. <span class="tag tag--example">Example</span> rows are placeholder data.')}
{AD()}
{section("maintenance","Wipers, battery, fuses &amp; towing",maint,kicker="Shown only when a source exists")}
{section("mpg","Fuel economy",fe,kicker="EPA city / highway / combined mpg")}
<div class="m-only">{section("problems","Common problems",probs,tools=False)}</div>
{feedback()}
{refs([f"{OM}. Page cited per figure.","fueleconomy.gov (U.S. EPA / DOE), 2020 Toyota RAV4, fetched 2026-10-15.","NHTSA recalls database, 2020 Toyota RAV4, fetched 2026-10-15."])}
</div><aside class="side">{panel("Common problems",probs)}{panel("Jump to",'<ul class="plist"><li><a href="#quick">Quick answer</a></li><li><a href="#recalls">Recalls</a></li><li><a href="#tires">Tire size &amp; pressure</a></li><li><a href="#maintenance">Parts &amp; fluids</a></li><li><a href="#mpg">Fuel economy</a></li><li><a href="#sources">Sources</a></li></ul>')}{AD("side")}</aside></div></div>'''

open('spec-2020-rav4.html','w').write(page("2020 Toyota RAV4 Specs: Oil Capacity, Tire Pressure, Fuses & Recalls | CarSpecFix","Specs",spec))

# ---------- ISSUE
def causes_list(items):
    if not items: return f'<span class="nv">{PEND}</span>'
    return '<ol class="causes">'+''.join(f'<li><div class="cause__src">{src}{(" "+tag("Example")) if ex else ""}</div><div class="cause__seen"><span class="fact__k" style="display:inline;margin:0">Seen on:</span> {seen}</div></li>' for src,seen,ex in items)+'</ol>'
def issue(cur,cr,eyebrow,title,code,defn,drive,srcs,causes=None,causes_kicker=''):
    nvq=f'<span class="nv">{PEND}</span>'
    qa=f'''<section class="qa" id="quick" data-copy-scope aria-label="Quick answer"><div class="qa__head"><h2 class="qa__title">Quick answer</h2><div class="tools"><button class="btn" data-copy="">{I("copy")}<span class="lbl">Copy</span></button><button class="btn" data-print>{I("print")}<span>Print</span></button></div></div>{f'<div class="qa__item" style="border-bottom:1px solid var(--border)"><div class="qa__q">What it means</div><div class="qa__a qa__a--text">{defn}</div><div class="qa__src">SAE J2012 generic definition · citable source not yet attached</div></div>' if defn else ''}<div class="qa__grid">
<div class="qa__item"><div class="qa__q">Can I keep driving?</div><div class="qa__a qa__a--text">{nvq}</div>{f'<div class="qa__more">{drive}</div>' if drive else ''}</div>
<div class="qa__item"><div class="qa__q">How urgent?</div><div class="qa__a qa__a--text">{tag("na")}</div><div class="qa__more">Severity not yet rated. Scale: {tag("Low")} {tag("Medium")} {tag("High")}</div></div>
<div class="qa__item"><div class="qa__q">Shop visit or check it yourself first?</div><div class="qa__a qa__a--text">{nvq}</div></div>
</div><div class="qa__foot"><span>Last verified <span class="tnum">2026-10-15</span></span><a href="#report">Report a data error</a></div></section>'''
    facts=f'<div class="facts"><div class="fact fact--full"><div class="fact__k">When to stop driving / get it checked</div><div class="fact__v"><span class="nv">{PEND}</span></div></div></div>'
    aff='<ul class="plist"><li><a href="spec-2020-rav4.html">2020 Toyota RAV4</a><span class="ks__src" style="margin:0">Specs</span></li></ul>'
    return f'''<div class="container"><div class="phead" style="padding-bottom:20px">{crumbs(*cr)}<div class="eyebrow" style="margin-top:8px">{eyebrow}</div><h1 class="ptitle">{title}</h1>{qa}</div>
<div class="layout"><div class="main">{section("causes","Possible causes",causes_list(causes),kicker=causes_kicker,tools=bool(causes))}
{section("details","What to do",facts,tools=False)}
<div class="m-only">{section("vehicles","Affected vehicles",aff,tools=False)}</div>
{feedback()}
{refs(srcs)}</div>
<aside class="side">{panel("Affected vehicles",aff)}{panel("Look up a code",'<form class="code-form" action="code-p0455.html"><label class="field"><span>OBD-II code</span><input placeholder="P0455"></label><button class="btn btn--primary" style="height:auto">Go</button></form>')}{AD("side")}</aside></div></div>'''
FMT_KICK='Each cause: source bulletin (manufacturer, bulletin no.) — seen on: model list. Rows tagged Example show the format only.'
open('symptom-brakes-squeaking.html','w').write(page("Brakes Squeaking: Causes, Is It Safe to Drive? | CarSpecFix","Symptoms",issue("Symptoms",[("Home","index.html"),("Symptoms","#"),("Brakes squeaking",None)],"Symptom · Brakes","Brakes squeaking: causes &amp; is it safe to drive?",None,None,"Brake issues: have it inspected promptly.",["No sourced causes yet. Causes are published only with a citable manufacturer bulletin or manual reference."],causes=None)))
open('code-p0455.html','w').write(page("P0455 Code: Meaning, Causes & Can You Keep Driving? | CarSpecFix","Trouble codes",issue("Trouble codes",[("Home","index.html"),("Trouble codes","#"),("P0455",None)],"OBD-II trouble code","P0455: meaning, causes &amp; can you keep driving?","P0455","Evaporative Emission System Leak Detected (large leak)",None,["SAE J2012 generic definition: citable public source not yet attached.","Cause bulletins: none attached yet. Causes are shown only with manufacturer and bulletin number."],causes=[(f'<span class="nv">Not yet verified</span> (manufacturer —, bulletin no. —)','<span class="muted">—</span>',False),('Source bulletin (Manufacturer, bulletin no. XXXX-XX)','2020 Toyota RAV4, other models from the bulletin',True)],causes_kicker=FMT_KICK)))
# ---------- HOME
yrs=''.join(f'<option{" selected" if y==2020 else ""}>{y}</option>' for y in range(2025,2014,-1))
def fld(l,inner): return f'<label class="field"><span>{l}</span>{inner}{I("chevron")}</label>'
cards=[("2020","Toyota RAV4","suv","Oil · Tires · MPG · Recalls",True),("2018","Toyota Camry","sedan","Coming soon",False),("2019","Honda CR-V","suv","Coming soon",False),("2017","Ford F-150","truck","Coming soon",False)]
vg=''.join(f'<{"a href=spec-2020-rav4.html" if on else "div"} class="vcard{"" if on else " vcard--soon"}"><div class="vcard__art"><img src="assets/car-{a}.svg" alt="" width="320" height="120"></div><div class="vcard__body"><span class="vcard__yr">{y}</span><span class="vcard__name">{n}</span><span class="vcard__meta">{m}</span></div></{"a" if on else "div"}>' for y,n,a,m,on in cards)
makes=["Chevrolet","Ford","Honda","Hyundai","Jeep","Kia","Nissan","Toyota"]
mk=''.join(f'<a class="make" href="spec-2020-rav4.html">{m}</a>' if m=="Toyota" else f'<span class="make">{m}</span>' for m in makes)
home=f'''<section class="finder"><div class="container"><h1>Car Specs by Year, Make &amp; Model: Oil, Tires, Recalls</h1><p>Oil capacity, tire pressure, fuses and recalls, with a source for every number.</p>
<div class="finder__tabs"><a href="#" aria-current="true">By vehicle</a><a href="code-p0455.html">By trouble code</a></div>
<form class="finder__form" action="spec-2020-rav4.html">{fld("Year",f"<select>{yrs}</select>")}{fld("Make","<select><option selected>Toyota</option><option>Honda</option><option>Ford</option><option>Chevrolet</option><option>Nissan</option></select>")}{fld("Model","<select><option>RAV4</option></select>")}<button class="btn btn--accent btn--lg" type="submit">Show specs</button></form></div></section>
<div class="container">
<section class="hsec"><div class="hsec__head"><h2 class="section__title">Popular vehicles</h2></div><div class="vgrid">{vg}</div></section>
<div class="split hsec">
<section><div class="hsec__head"><h2 class="section__title">Check a trouble code</h2></div><form class="code-form" action="code-p0455.html"><label class="field"><span>OBD-II code</span><input class="mono" placeholder="P0455"></label><button class="btn btn--primary btn--lg" style="height:auto">Check code</button></form><p class="ks__src" style="margin-top:8px">Generic SAE J2012 definitions. Causes shown only when sourced.</p></section>
<section><div class="hsec__head"><h2 class="section__title">What's wrong with my car?</h2></div><ul class="links"><li><a href="symptom-brakes-squeaking.html">Brakes squeaking</a>{tag("na")}</li><li><span>Car shakes when braking</span><span class="ks__src" style="margin:0">Coming soon</span></li><li><span>Grinding noise when braking</span><span class="ks__src" style="margin:0">Coming soon</span></li><li><span>Check engine light</span><span class="ks__src" style="margin:0">Coming soon</span></li></ul></section></div>
<section class="hsec"><div class="hsec__head"><h2 class="section__title">Browse by make</h2></div><div class="makes">{mk}</div></section>
<div class="hsec">{feedback()}</div>
</div>'''
open('index.html','w').write(page("Car Specs by Year, Make & Model: Oil, Tires, Recalls | CarSpecFix","",home))

# ---------- GALLERY
g=f'''<div class="container">{crumbs(("Home","index.html"),("Components",None))}<h1 class="ptitle">Components</h1><div class="layout"><div class="main">
{section("g-btn","Buttons &amp; chips",f'<div class="chips"><button class="btn btn--accent btn--lg">Show specs</button><button class="btn btn--primary">Check code</button>{COPY()}<button class="btn" data-print>{I("print")}<span>Print</span></button></div><div class="chips" style="margin-top:12px"><a class="chip" aria-current="page">2020</a><a class="chip chip--muted">2021</a><span class="chip">AWD</span></div>',tools=False)}
{section("g-sev","Severity tags",f'<div class="chips">{tag("Low")}{tag("Medium")}{tag("High")}{tag("na")}{tag("Example")}</div>',tools=False)}
{section("g-ks","Key specs strip (figure + source)",strip,tools=False)}
{section("g-qa","Quick answer (issue pages)",'<div class="qa"><div class="qa__grid"><div class="qa__item"><div class="qa__q">Can I keep driving?</div><div class="qa__a qa__a--text"><span class="nv">Not yet verified — source pending</span></div></div><div class="qa__item"><div class="qa__q">How urgent?</div><div class="qa__a qa__a--text">'+tag("na")+'</div></div><div class="qa__item"><div class="qa__q">Shop visit or check it yourself first?</div><div class="qa__a qa__a--text"><span class="nv">Not yet verified — source pending</span></div></div></div></div>',tools=False)}
{section("g-causes","Cause list (source bulletin + seen on)",causes_list([("Source bulletin (Manufacturer, bulletin no. XXXX-XX)","2020 Toyota RAV4, other models from the bulletin",True)]),tools=False)}
{section("g-kv","Spec list",'<div class="kv">'+kvrow("Oil capacity, with filter","4.8","qt / 4.5 L","manual p.666",1)+kvrow("Battery group size")+'</div>',tools=False)}
{section("g-tires","Multi-row spec table (tires)",tires,kicker="Scrolls sideways below 1024px")}
{section("g-rc","Data table",rc)}
{section("g-n","Notice",f'<div class="notice">{I("warning")}<span>The model year of manual OM0R024U is not yet confirmed.</span></div>',tools=False)}
{section("g-ad","Ad slots (below tables / sidebar only)",AD()+'<div style="height:12px"></div>'+AD("side"),tools=False)}
{section("g-card","Vehicle card",f'<div class="vgrid">{vg}</div>',tools=False)}
{section("g-hf","Header, sub-nav &amp; footer",'<p class="vsub" style="margin:0">Sticky header with search is at the top of this page. The sub-nav is shown on the spec page. The footer is at the bottom.</p>',tools=False)}
{section("g-ic","Icons &amp; art (assets/)",'<div class="chips">'+''.join(f'<span class="chip" style="gap:6px">{I(k)}{k}</span>' for k in SV)+'</div><div class="vgrid" style="margin-top:12px">'+''.join(f'<div class="vcard"><div class="vcard__art"><img src="assets/car-{a}.svg" alt="{a}"></div></div>' for a in ("suv","sedan","truck"))+'<div class="vcard"><div class="vcard__art"><img src="assets/logo.svg" alt="logo" style="width:56px"></div></div></div>',tools=False)}
</div></div></div>'''
open('components.html','w').write(page("Components | CarSpecFix","",g))
