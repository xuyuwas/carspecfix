import sys,json;sys.path.insert(0,'/workspace/keyword-scan')
import serp
from urllib.parse import urlparse
T=["2020 rav4 oil capacity","2018 camry tire pressure","2017 f150 fuse box diagram","2015 silverado p0420","f150 p0455","2018 camry shakes when braking","2016 honda civic battery size","alternator replacement cost honda accord"]
res={}
for t in T:
    u=serp._brave(t) or []
    if isinstance(u,dict): u=u.get("urls",[])
    res[t]=u[:10]; print(t,[urlparse(x).hostname for x in u[:10]],flush=True)
json.dump(res,open("/workspace/carspecfix/serp_lt.json","w"),indent=1)
