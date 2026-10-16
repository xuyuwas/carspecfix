import requests,json,time,random,os,concurrent.futures as cf,threading
M=["toyota rav4","toyota camry","toyota corolla","toyota tacoma","toyota highlander","toyota tundra","toyota 4runner","toyota prius","toyota sienna",
"honda cr-v","honda civic","honda accord","honda pilot","honda odyssey","honda hr-v",
"ford f150","ford escape","ford explorer","ford mustang","ford ranger","ford bronco","ford edge","ford fusion",
"chevy silverado","chevy equinox","chevy tahoe","chevy malibu","chevy colorado","chevy traverse",
"tesla model y","tesla model 3","nissan altima","nissan rogue","nissan sentra","jeep wrangler","jeep grand cherokee","ram 1500","subaru outback","subaru forester","subaru crosstrek","hyundai tucson","hyundai elantra","kia sportage","mazda cx-5","gmc sierra"]
A=["oil capacity","oil type","tire size","tire pressure","wiper size","battery size","fuse box","recalls","towing capacity","mpg"]
S=["grinding noise when braking","brakes squeaking","shakes when braking","shaking when accelerating","jerks when accelerating","cranks but wont start","check engine light","ac not blowing cold","engine ticking noise","p0420","p0300","p0171","p0455","p0442","p0456"]
qs=[f"{y} {m.split(' ',1)[1]} {a}" for m in M for y in range(2015,2026) for a in A]+[f"{m} {s}" for m in M for s in S]
out=json.load(open('suggest_v3.json')) if os.path.exists('suggest_v3.json') else {}
qs=[q for q in qs if q not in out]; print(len(qs),flush=True)
lock=threading.Lock(); fails=[0]
def g(q):
    for t in range(3):
        if fails[0]>=25: return q,None
        time.sleep(random.uniform(0.4,0.9))
        try:
            r=requests.get("https://suggestqueries.google.com/complete/search",params={"client":"firefox","q":q,"hl":"en","gl":"us"},timeout=10)
            if r.status_code==200: fails[0]=max(0,fails[0]-1); return q,r.json()[1]
            fails[0]+=1; time.sleep(10*(t+1))
        except Exception: fails[0]+=1; time.sleep(5)
    return q,None
n=0
with cf.ThreadPoolExecutor(4) as ex:
    for q,l in ex.map(g,qs):
        n+=1
        if l is not None: out[q]=l
        if n%200==0:
            json.dump(out,open('suggest_v3.json','w')); print(n,len(out),fails[0],flush=True)
json.dump(out,open('suggest_v3.json','w')); print('done',len(out),'stopped' if fails[0]>=25 else 'ok')
