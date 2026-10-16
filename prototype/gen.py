import json,csv,html
B='/workspace/carspecfix/'
spec=json.load(open(B+'spec_api_data.json'));sym=json.load(open(B+'symptom_pages.json'))
rows={r['slug']:r for r in csv.DictReader(open(B+'spec_pages.csv'))}
e=html.escape
TODO='<span class="text-amber-700 font-semibold">Not yet verified — check owner\'s manual</span>'
def v(x): return TODO if (not x or x.strip().upper().startswith('TODO')) else e(x)
def page(title,desc,body,crumbs,ld):
    bc=' › '.join(f'<a class="hover:underline" href="{u}">{e(n)}</a>' for n,u in crumbs)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><script src="https://cdn.tailwindcss.com"></script>
<script type="application/ld+json">{json.dumps(ld)}</script>
<style>@media print{{.noprint{{display:none}}}}</style></head><body class="bg-white text-slate-800">
<header class="bg-blue-900 text-white"><div class="max-w-5xl mx-auto px-4 py-3 flex justify-between items-center"><a href="index.html" class="font-extrabold text-xl">CarSpec<span class="text-amber-400">Fix</span></a>
<nav class="text-sm space-x-4 hidden sm:block"><a href="#">Specs</a><a href="symptom-brakes-squeaking.html">Symptoms</a><a href="code-p0455.html">Codes</a><a href="#">Maintenance</a></nav></div></header>
<main class="max-w-5xl mx-auto px-4 py-6"><div class="text-xs text-slate-500 mb-3">{bc}</div>{body}</main>
<footer class="border-t mt-10 text-xs text-slate-500"><div class="max-w-5xl mx-auto px-4 py-6">Data from owner's manuals, NHTSA, fueleconomy.gov and RepairPal — every number cites its source. <a class="underline" href="#">Data sources</a> · <a class="underline" href="#">About</a> · <a class="underline" href="#">Privacy</a> · <a class="underline" href="#">Contact</a></div></footer>
<script>function cp(id){{navigator.clipboard.writeText(document.getElementById(id).innerText)}}</script></body></html>'''
AD='<div class="noprint my-6 border-2 border-dashed border-slate-300 text-slate-400 text-center text-xs py-8">Ad slot (below table only)</div>'
def bcld(c): return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":"https://carspecfix.com"+u} for i,(n,u) in enumerate(c)]}
# HOME
makes=['Toyota','Honda','Ford','Chevrolet','Nissan']
home=f'''<section class="text-center py-6"><h1 class="text-3xl sm:text-4xl font-extrabold text-blue-900">Car Specs by Year, Make &amp; Model</h1>
<p class="mt-2 text-slate-600">Oil capacity, tire pressure, fuses, recalls — plus what your warning light or noise means.</p></section>
<div class="grid gap-4 md:grid-cols-3">
<form class="md:col-span-3 bg-slate-50 border rounded-xl p-4 grid gap-2 sm:grid-cols-4" action="spec-2020-toyota-rav4.html">
<select class="border rounded-lg p-3"><option>Year</option>{''.join(f'<option>{y}</option>' for y in range(2025,2014,-1))}</select>
<select class="border rounded-lg p-3"><option>Make</option>{''.join(f'<option>{m}</option>' for m in makes)}</select>
<select class="border rounded-lg p-3"><option>Model</option><option>RAV4</option></select>
<button class="bg-amber-500 hover:bg-amber-600 text-blue-950 font-bold rounded-lg p-3">Show specs</button></form>
<form class="border rounded-xl p-4" action="code-p0455.html"><h2 class="font-bold text-blue-900">Look up a trouble code</h2><input class="mt-2 w-full border rounded-lg p-3 uppercase" placeholder="e.g. P0455"><button class="mt-2 w-full bg-blue-900 text-white rounded-lg p-3 font-semibold">Check code</button></form>
<div class="border rounded-xl p-4 md:col-span-2"><h2 class="font-bold text-blue-900">What's wrong with my car?</h2><div class="mt-2 flex flex-wrap gap-2">
{''.join(f'<a href="symptom-brakes-squeaking.html" class="px-3 py-2 rounded-full bg-slate-100 text-sm">{x}</a>' for x in ['Brakes squeaking','Car shakes when braking','Grinding noise when braking','Check engine light'])}</div></div></div>
<h2 class="mt-8 font-bold text-blue-900">Popular vehicles</h2><div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-2">
<a href="spec-2020-toyota-rav4.html" class="border rounded-lg p-3 hover:border-amber-500">2020 Toyota RAV4</a>
{''.join(f'<div class="border rounded-lg p-3 text-slate-400">{s} (coming soon)</div>' for s in ['2018 Toyota Camry','2019 Honda CR-V','2017 Ford F-150'])}</div>'''
open('index.html','w').write(page('Car Specs by Year, Make & Model – Oil, Tires, Fuses & Fixes | CarSpecFix','Look up car specs by year, make and model: oil capacity, tire size and pressure, fuses, towing, MPG and recalls, with sources.',home,[('Home','/')],{"@context":"https://schema.org","@type":"WebSite","name":"CarSpecFix","url":"https://carspecfix.com/"}))
# SPEC
r=rows['2020-toyota-rav4'];d=spec[0]
def card(id,label,val,src):
    return f'''<div class="border rounded-xl p-4"><div class="flex justify-between"><div class="text-xs uppercase tracking-wide text-slate-500">{label}</div><button onclick="cp('{id}')" class="noprint text-xs text-blue-800">Copy</button></div>
<div id="{id}" class="mt-1 text-2xl font-extrabold text-blue-950">{val}</div><div class="mt-1 text-xs text-slate-500">Source: {src}</div></div>'''
man=f'<a class="underline" href="{e(r["manual_source"])}">Toyota owner\'s manual OM0R024U</a> <span class="text-amber-700">(model year to be confirmed)</span>'
cards=''.join([card('oil','Oil capacity (with filter)','4.8 qt <span class="text-base font-semibold text-slate-500">/ 4.5 L</span>',man+', p.666'),
card('visc','Oil viscosity','SAE 0W-16 <span class="text-base font-semibold text-slate-500">(0W-20 acceptable)</span>',man+', p.667'),
card('tire','Tire size (17-in type A)','225/65R17 102H',man+', p.671'),
card('psi','Tire pressure (type A)','35 psi <span class="text-base font-semibold text-slate-500">/ 241 kPa / 2.4 bar</span>',man+', p.671 · metric converted'),
card('wip','Wiper blade sizes',TODO,'—'),card('bat','Battery group size',TODO,'—'),card('fuse','Fuse box diagram',TODO,'—'),card('tow','Towing capacity',TODO,'—')])
fe=''.join(f'<tr class="border-t"><td class="p-2">{e(x["model"])}</td><td class="p-2">{e(x["option"])}</td><td class="p-2">{e(x["drive"])}</td><td class="p-2 font-bold">{x["mpg_city"]}/{x["mpg_hwy"]}/{x["mpg_comb"]}</td></tr>' for x in d['fueleconomy'])
rc=''.join(f'<tr class="border-t"><td class="p-2 font-mono">{x["campaign"]}</td><td class="p-2">{e(x["component"])}</td><td class="p-2">{x["date"]}</td></tr>' for x in d['recalls'])
body=f'''<h1 class="text-2xl sm:text-3xl font-extrabold text-blue-900">2020 Toyota RAV4 Specs: Oil, Tires, Fuses &amp; Recalls</h1>
<p class="text-sm text-slate-500 mt-1">Updated 2026-10-15 · Every number links to its source · <button onclick="print()" class="noprint underline">Print</button></p>
<div class="mt-3 p-3 bg-amber-50 border border-amber-300 rounded-lg text-sm">⚠ Manual model year is not yet confirmed. Verify against your own owner's manual before relying on these values.</div>
<div class="grid sm:grid-cols-2 gap-3 mt-4">{cards}</div>{AD}
<h2 class="text-xl font-bold text-blue-900 mt-6">Fuel economy (city/hwy/combined mpg)</h2><div class="overflow-x-auto"><table class="w-full text-sm mt-2"><thead class="bg-slate-100 text-left"><tr><th class="p-2">Model</th><th class="p-2">Engine/trans</th><th class="p-2">Drive</th><th class="p-2">MPG</th></tr></thead><tbody>{fe}</tbody></table></div>
<p class="text-xs text-slate-500">Source: <a class="underline" href="{e(d['fueleconomy'][0]['source'])}">fueleconomy.gov</a> (EPA), fetched 2026-10-15</p>
<h2 class="text-xl font-bold text-blue-900 mt-6">Recalls ({len(d['recalls'])})</h2><div class="overflow-x-auto"><table class="w-full text-sm mt-2"><thead class="bg-slate-100 text-left"><tr><th class="p-2">NHTSA campaign</th><th class="p-2">Component</th><th class="p-2">Date (DD/MM/YYYY)</th></tr></thead><tbody>{rc}</tbody></table></div>
<p class="text-xs text-slate-500">Source: <a class="underline" href="{e(d['recalls_source'])}">NHTSA</a>, fetched 2026-10-15. Check your VIN at nhtsa.gov/recalls.</p>
<h2 class="text-xl font-bold text-blue-900 mt-6">Common problems</h2><ul class="list-disc ml-5 text-sm mt-2"><li><a class="text-blue-800 underline" href="symptom-brakes-squeaking.html">Brakes squeaking</a></li><li><a class="text-blue-800 underline" href="code-p0455.html">P0455 – EVAP large leak</a></li></ul>
<h2 class="text-xl font-bold text-blue-900 mt-6">TPMS reset</h2><p class="text-sm mt-2">{TODO}</p>'''
c=[('Home','/'),('Specs','/specs/'),('Toyota','/specs/toyota/'),('RAV4','/specs/toyota/rav4/'),('2020','/specs/toyota/rav4/2020/')]
open('spec-2020-toyota-rav4.html','w').write(page('2020 Toyota RAV4 Specs: Oil Capacity, Tire Pressure, Fuses & Recalls | CarSpecFix','2020 Toyota RAV4 oil capacity (4.8 qt with filter), tire size, tire pressure, MPG and 6 NHTSA recalls — each value with its source.',body,c,{"@context":"https://schema.org","@graph":[{"@type":"Vehicle","name":"2020 Toyota RAV4","brand":"Toyota","model":"RAV4","vehicleModelDate":"2020"},bcld(c)]}))
# SYMPTOM / CODE
def issue(x,fname,h1,crumbs):
    costs=''.join(f'<tr class="border-t"><td class="p-2">{e(k["repair"])}</td><td class="p-2 font-bold">{v(k["range_usd"])}</td><td class="p-2 text-xs">{"<a class=underline href="+e(k["source"])+">RepairPal</a> · "+e(k.get("source_date","")) if k["source"].startswith("http") else TODO}</td></tr>' for k in x['costs'])
    sev='<span class="inline-block px-2 py-1 rounded bg-slate-200 text-xs font-bold">Severity: not yet rated</span> <span class="text-xs text-slate-500">(badges: <span class="px-1 rounded bg-green-100 text-green-800">Low</span> <span class="px-1 rounded bg-yellow-100 text-yellow-800">Medium</span> <span class="px-1 rounded bg-red-100 text-red-800">High</span>)</span>'
    defn='' if not x['code_definition'] else f'<div class="mt-4 border rounded-xl p-4"><div class="text-xs uppercase text-slate-500">Definition (SAE J2012 generic)</div><div class="text-xl font-extrabold text-blue-950">Evaporative Emission System Leak Detected (large leak)</div><div class="text-xs text-amber-700">Citable public source: not yet attached</div></div>'
    body=f'''<h1 class="text-2xl sm:text-3xl font-extrabold text-blue-900">{h1}</h1><div class="mt-2">{sev}</div>{defn}
<div class="grid sm:grid-cols-2 gap-3 mt-4"><div class="border rounded-xl p-4"><h2 class="font-bold text-blue-900">Possible causes</h2><p class="text-sm mt-1">{TODO.replace("check owner's manual","source pending")}</p></div>
<div class="border rounded-xl p-4"><h2 class="font-bold text-blue-900">Can I still drive?</h2><p class="text-sm mt-1">{TODO.replace("check owner's manual","source pending")}{" Brake issues: have it inspected promptly." if "brake" in x["slug"] else ""}</p></div></div>
<h2 class="text-xl font-bold text-blue-900 mt-6">Repair cost (US national average)</h2><div class="overflow-x-auto"><table class="w-full text-sm mt-2"><thead class="bg-slate-100 text-left"><tr><th class="p-2">Repair</th><th class="p-2">Range</th><th class="p-2">Source</th></tr></thead><tbody>{costs}</tbody></table></div>{AD}
<h2 class="text-xl font-bold text-blue-900 mt-6">Affected vehicles</h2><a class="text-blue-800 underline text-sm" href="spec-2020-toyota-rav4.html">2020 Toyota RAV4 specs</a>'''
    open(fname,'w').write(page(h1+' | CarSpecFix',h1,body,crumbs,{"@context":"https://schema.org","@graph":[bcld(crumbs)]}))
S={x['slug']:x for x in sym}
issue(S['brakes-squeaking'],'symptom-brakes-squeaking.html','Brakes Squeaking: Causes, Can You Drive &amp; Repair Cost'.replace('&amp;','&'),[('Home','/'),('Symptoms','/symptoms/'),('Brakes squeaking','/symptoms/brakes-squeaking/')])
issue(S['p0455'],'code-p0455.html','P0455 Code: Meaning, Causes & Repair Cost',[('Home','/'),('Codes','/codes/'),('P0455','/codes/p0455/')])
