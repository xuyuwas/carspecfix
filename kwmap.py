import re,csv,json,collections,pandas as pd
kws=[l.strip().lower() for l in open('keywords.csv') if l.strip()]
raw=len(kws)
def norm(k):
    k=re.sub(r"[’']",'',k); k=re.sub(r'(?<=[a-z])\.(?=[a-z])',' ',k); k=re.sub(r'\s+',' ',k).strip()
    k=re.sub(r'\bf[- ]?(150|250|350)\b',r'f-\1',k)
    k=re.sub(r'\bcr[- ]?v\b','cr-v',k); k=re.sub(r'\bhr[- ]?v\b','hr-v',k)
    k=re.sub(r'\brav ?4\b','rav4',k); k=re.sub(r'\bwont\b','won\'t',k).replace("won't",'wont')
    k=re.sub(r'\bchevy\b','chevrolet',k)
    k=re.sub(r'\bmodel ?y\b','model y',k); k=re.sub(r'\bmodel ?3\b','model 3',k)
    return k
MODELS={'rav4':'toyota','camry':'toyota','corolla':'toyota','tacoma':'toyota','tundra':'toyota','highlander':'toyota','4runner':'toyota','prius':'toyota','sienna':'toyota',
'cr-v':'honda','civic':'honda','accord':'honda','pilot':'honda','odyssey':'honda','hr-v':'honda',
'f-150':'ford','f-250':'ford','escape':'ford','explorer':'ford','mustang':'ford','ranger':'ford','bronco':'ford','edge':'ford','fusion':'ford',
'silverado':'chevrolet','equinox':'chevrolet','tahoe':'chevrolet','malibu':'chevrolet','colorado':'chevrolet','traverse':'chevrolet',
'model y':'tesla','model 3':'tesla','altima':'nissan','rogue':'nissan','sentra':'nissan','wrangler':'jeep','grand cherokee':'jeep','cherokee':'jeep',
'ram 1500':'ram','outback':'subaru','forester':'subaru','crosstrek':'subaru','elantra':'hyundai','tucson':'hyundai','sorento':'kia','sportage':'kia','cx-5':'mazda','sierra':'gmc'}
MAKES=['toyota','honda','ford','chevrolet','tesla','nissan','jeep','ram','subaru','hyundai','kia','mazda','gmc','dodge','bmw','audi','mercedes','volkswagen','vw','lexus','acura','infiniti','buick','cadillac','chrysler','volvo','mitsubishi','lincoln']
NOISE=r'\b(costco|gx\d+|d1[123]|outboard|for sale|price|prices|msrp|dome|city|fire department|lawyer|legal|accord(s)? (definition|meaning)|interior|exterior|colors?|release date|wiki|review|reviews|dimensions|cargo|lease|used|near me|camper|shell|rental|news|hotel|weather|zip code|county|mall|airport|jobs|z\d{3}|gcv\d+|mower|generator|motorcycle|atv|boat|lawn|juniper|wallpaper|toy|lego|game|shirt)\b'
ATTR=[('oil capacity',r'oil capacity|how much oil|quarts? of oil|oil quantity'),('oil type',r'oil type|what oil|oil weight|oil viscosity|type of oil|which oil|synthetic oil|\boil (?:for|does)'),
('tire pressure',r'tire pressure|tyre pressure|\bpsi\b'),('tire size',r'tire size|tyre size|rim size|wheel size|bolt pattern|lug nut'),
('fuse box',r'fuse'),('towing capacity',r'towing|tow capacity|payload'),('recalls',r'recall'),('battery',r'battery'),('wiper',r'wiper'),
('mpg',r'\bmpg\b|gas mileage|fuel economy|miles per gallon'),('engine/specs',r'horsepower|\bhp\b|engine size|specs|torque|gas tank|fuel tank|tank size|coolant type|transmission fluid|headlight bulb|bulb size|serpentine|spark plug gap|firing order')]
SYM=[('brakes-squeaking',r'squeak|squeal(?!ing noise when driving)'),('grinding-noise-when-braking',r'grind'),('car-shakes-when-braking',r'(shak|vibrat|wobbl|pulsat)\w* (when|while) (braking|stopping)'),
('car-shaking-when-accelerating',r'(shak|vibrat)\w* (when|while) accelerat'),('car-jerks-when-accelerating',r'jerk|hesitat|lurch'),('car-cranks-but-wont-start',r'cranks? but|turns? over but'),
('car-wont-start-clicking',r'(wont start|no start).*click|click.*(wont start)|clicking noise'),('abs-light-on',r'\babs\b'),('check-engine-light',r'check engine'),
('engine-ticking-noise',r'\btick'),('car-vibration-at-high-speed',r'(shak|vibrat)\w*.*(high|highway|speed|mph)'),('car-ac-not-blowing-cold',r'\bac\b|a/c|air condition'),
('burning-smell',r'burn\w* smell|smells? like'),('brake-pedal-to-floor',r'pedal'),('tire-pressure-light',r'tire pressure (light|sensor|monitor)|tpms'),('car-wont-start',r'wont start|not starting|no start')]
COST=r'\bcost|price to (fix|replace)|how much (to|does it cost)|estimate'
HOWTO=r'^how to|\bhow do i\b|\breplacement\b(?!.*cost)|\bchange\b|\breset\b|\bdiy\b|\binstall|\bclear\b'
def slug(s): return re.sub(r'[^a-z0-9]+','-',s).strip('-')
rows=[];seen=set();drop=collections.Counter()
for k0 in kws:
    k=norm(k0)
    if k in seen: drop['dup']+=1;continue
    seen.add(k)
    model=next((m for m in sorted(MODELS,key=len,reverse=True) if re.search(r'\b'+re.escape(m)+r'\b',k)),'')
    make=MODELS.get(model,'') or next((m for m in MAKES if re.search(r'\b'+m+r'\b',k)),'')
    ym=re.search(r'\b(19[89]\d|20[0-2]\d)\b',k); year=ym.group(1) if ym else ''
    code=re.search(r'\b([pbcu]\d{4})\b',k)
    attr=next((a for a,p in ATTR if re.search(p,k)),'')
    sym=next((s for s,p in SYM if re.search(p,k)),'')
    if attr=='tire pressure' and sym=='tire-pressure-light': attr=''
    noise=re.search(NOISE,k)
    if code: sec='codes'; a=code.group(1)
    elif re.search(COST,k): sec='repair cost'; a=''
    elif sym: sec='symptoms'; a=sym
    elif re.search(HOWTO,k) and (attr or make): sec='maintenance how-to'; a=attr
    elif attr: sec='specs'; a=attr
    else: drop['noise/no car intent']+=1; continue
    if sec=='repair cost' and not (make or model or re.search(r'\b(car|brake|engine|transmission|alternator|starter|catalytic|radiator|head gasket|timing|strut|shock|axle|clutch|tire|rotor|ac compressor|water pump|fuel pump|o2|oxygen|spark|coil|evap|misfire|coolant|exhaust|muffler|battery|wheel bearing|suspension|serpentine|thermostat|bumper|windshield)\b',k)): drop['repair cost non-car']+=1; continue
    if noise and sec!='codes' and not (sec=='specs' and noise.group(0) in('dimensions',)): drop['noise pattern']+=1; continue
    if sec in('specs','maintenance how-to') and not (make or model): drop['spec without vehicle']+=1; continue
    # URL
    msl=('silverado-1500' if model=='silverado' else slug(model)) if model else ''
    if sec=='specs':
        url=f'/specs/{make}/{msl}/{year}/' if (model and year) else (f'/specs/{make}/{msl}/' if model else f'/specs/{make}/')
        intent='informational-lookup'
    elif sec=='codes':
        url=f'/codes/{a}/'; intent='diagnostic'
    elif sec=='symptoms':
        url=f'/symptoms/{a}/'; intent='diagnostic'
    elif sec=='repair cost':
        part=re.sub(COST,'',k); 
        for w in [model,make,year]+MAKES:
            if w: part=re.sub(r'\b'+re.escape(w)+r'\b','',part)
        part=re.sub(r'\b(to|a|the|of|fix|replace|for|on|my|does it|how much|repair|replacement|average|car)\b','',part)
        part=slug(part) or 'general'; a=part
        url=f'/repair-cost/{part}/'; intent='commercial'
    else:
        url=f'/specs/{make}/{msl}/{year}/' if (model and year) else (f'/how-to/{slug(a or "general")}/' if not model else f'/specs/{make}/{msl}/')
        intent='how-to'
    rows.append(dict(keyword=k,section=sec,attribute=a or attr,make=make,model=model,year=year,intent=intent,target_url=url))
df=pd.DataFrame(rows)
# merge sparse repair-cost pages (<3 kws) into /repair-cost/ hub
c=df[df.section=='repair cost'].target_url.value_counts()
df.loc[df.target_url.isin(c[c<2].index),'target_url']='/repair-cost/'
sp=pd.read_csv('spec_pages.csv'); P1=set(sp.url)|{x['url'] for x in json.load(open('symptom_pages.json'))}
PILOTKW={x['url']:x['target_keyword'].lower().replace("won't",'wont') for x in json.load(open('symptom_pages.json'))}
# primary: shortest generic kw, preferring "{year} {model} specs" style; pilot pages use set kw
prim={}
for u,g in df.groupby('target_url'):
    if u in PILOTKW: prim[u]=PILOTKW[u]; continue
    p=u.strip('/').split('/')
    if u.startswith('/symptoms/'): prim[u]=p[1].replace('-',' '); continue
    if u.startswith('/repair-cost/') and len(p)>1: prim[u]=p[1].replace('-',' ')+' replacement cost'; continue
    if u.startswith('/specs/') and len(p)==4: prim[u]=f"{p[3]} {p[1]} {p[2].replace('-',' ')} specs"; continue
    if u=='/repair-cost/': prim[u]='car repair cost'; continue
    if u.startswith('/specs/') and len(p)==2: prim[u]=f"{p[1]} specs"; continue
    if u.startswith('/specs/') and len(p)==3: prim[u]=f"{p[1]} {p[2].replace('-',' ')} specs"; continue
    cand=g.copy(); cand['l']=cand.keyword.str.len()
    pref=cand[cand.keyword.str.contains('oil capacity|tire size|specs')] if u.startswith('/specs/') else cand
    prim[u]=(pref if len(pref) else cand).sort_values('l').keyword.iloc[0]
for u in P1:
    if u not in prim: prim[u]=PILOTKW.get(u,'')
df['role']=['primary' if prim[u]==k else 'secondary' for k,u in zip(df.keyword,df.target_url)]
# add pilot primaries missing in pool
add=[]
for u in list(P1)+[u for u in prim if u not in P1]:
    if not ((df.target_url==u)&(df.role=='primary')).any():
        if u not in P1:
            g=df[df.target_url==u].iloc[0]; add.append(dict(keyword=prim[u],section=g.section,attribute='',make=g.make,model=g.model,year=g.year,intent=g.intent,target_url=u,role='primary',source='seed (head term, not in pool)')); continue
        r=sp[sp.url==u]
        kw=PILOTKW.get(u) or f"{int(r.year.iloc[0])} {r.model.iloc[0].lower()} specs"
        prim[u]=kw
        sec='specs' if u.startswith('/specs') else ('codes' if u.startswith('/codes') else 'symptoms')
        add.append(dict(keyword=kw,section=sec,attribute='',make=u.split('/')[2] if sec=='specs' else '',model='',year='',intent='',target_url=u,role='primary',source='seed (not in autosuggest pool)'))
df['source']='autosuggest'; df=pd.concat([df,pd.DataFrame(add)],ignore_index=True)
# priority
cnt=df.target_url.value_counts()
TOPM={'rav4','camry','cr-v','f-150','civic','silverado','model y','equinox','corolla','tacoma','accord'}
def pri(u):
    if u in P1: return 'P1'
    p=u.split('/')
    if u.startswith('/specs/'):
        yr=p[4] if len(p)>5 and p[4] else ''
        mod=p[3].replace('-',' ') if len(p)>4 else ''
        if yr and int(yr)>=2012 and cnt[u]>=3: return 'P2'
        if not yr and len(p)>4 and p[3] and cnt[u]>=10: return 'P2'
        return 'P3'
    if u.startswith('/codes/') or u.startswith('/symptoms/'): return 'P2' if cnt[u]>=5 else 'P3'
    return 'P3'  # repair cost (repairpal dominates), how-to
pg=pd.DataFrame({'target_url':cnt.index,'n':cnt.values}); pg['priority']=pg.target_url.map(pri)
# cap P2 to ~200 by kw count
p2=pg[pg.priority=='P2'].sort_values('n',ascending=False)
pg.loc[p2.index[200:],'priority']='P3'
pm=dict(zip(pg.target_url,pg.priority)); df['priority']=df.target_url.map(pm)
pg['primary_keyword']=pg.target_url.map(prim); pg['n_secondary']=pg.n-1
pg['section']=pg.target_url.map(df.groupby('target_url').section.first())
pg=pg.sort_values(['priority','n'],ascending=[True,False])[['target_url','section','primary_keyword','n_secondary','priority']]
df=df.sort_values(['priority','target_url','role','keyword'])
cols=['keyword','section','attribute','make','model','year','intent','target_url','role','priority','source']
df[cols].to_csv('keyword_map.csv',index=False); pg.to_csv('pages.csv',index=False)
with pd.ExcelWriter('keyword_map.xlsx') as w:
    s=df.pivot_table(index='section',columns='priority',values='keyword',aggfunc='count',fill_value=0,margins=True)
    s.to_excel(w,sheet_name='summary'); pg.to_excel(w,sheet_name='pages',index=False)
    for sec,g in df.groupby('section'): g[cols].to_excel(w,sheet_name=sec[:31].replace('/','-'),index=False)
json.dump(dict(raw=raw,drop=drop,kept=len(df),seeds=len(add),sec=df.section.value_counts().to_dict(),kwpri=df.priority.value_counts().to_dict(),pagepri=pg.priority.value_counts().to_dict(),pages=len(pg),pagesec={f'{a}|{b}':int(v) for (a,b),v in pg.groupby(['section','priority']).size().items()}),open('kwmap_stats.json','w'),default=str,indent=1)
print(open('kwmap_stats.json').read()); print(pg.head(45).to_string())
