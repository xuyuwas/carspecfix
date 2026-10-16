import requests,json,string,concurrent.futures as cf,csv
seeds=["rav4","camry","cr-v","f150","civic","corolla","silverado","accord","tacoma","model y",
"brakes squeaking","car shakes when braking","grinding noise when braking","car shaking when accelerating","car jerks when accelerating","check engine light","car ac not blowing cold air","car cranks but wont start","engine ticking noise","burning smell from car",
"p0420","p0455","p0300","p0171","p0442",
"oil capacity","tire pressure","wiper blade size","battery size","fuse box","towing capacity",
"cost to fix","replacement cost"]
def g(q):
    try:
        r=requests.get("https://suggestqueries.google.com/complete/search",params={"client":"firefox","q":q,"hl":"en","gl":"us"},timeout=10)
        return q,r.json()[1]
    except Exception as e: return q,[]
qs=[s+" "+c for s in seeds for c in [""]+list(string.ascii_lowercase)]
res={}
with cf.ThreadPoolExecutor(16) as ex:
    for q,l in ex.map(g,qs): res[q]=l
out={}
for s in seeds:
    st=set()
    for c in [""]+list(string.ascii_lowercase): st.update(res[(s+" "+c)])
    out[s]=sorted(st)
json.dump(out,open("suggest.json","w"),indent=1)
allk=sorted({k for v in out.values() for k in v})
print(len(allk)); [print(s,len(v),v[:6]) for s,v in out.items()]
