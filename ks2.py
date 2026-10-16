import requests,json,concurrent.futures as cf
attrs=["oil capacity","oil type","tire size","tire pressure","wiper size","battery size","fuse box","recalls","towing capacity","mpg","p0420","grinding noise when braking","shaking when braking","cranks but wont start"]
models=["2020 rav4","2018 camry","2019 honda cr-v","2017 f150","2016 honda civic","2015 silverado"]
def g(q):
    try: return q,requests.get("https://suggestqueries.google.com/complete/search",params={"client":"firefox","q":q,"hl":"en","gl":"us"},timeout=10).json()[1]
    except: return q,[]
qs=[m+" "+a for m in models for a in attrs]
with cf.ThreadPoolExecutor(16) as ex: r=dict(ex.map(g,qs))
json.dump(r,open("suggest_ymm.json","w"),indent=1)
for q,l in r.items(): print(f"{q} | {len(l)} | {l[:3]}")
