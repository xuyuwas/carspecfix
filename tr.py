from pytrends.request import TrendReq
import time,json
heads=["tire pressure","oil capacity","towing capacity","fuse box diagram","wiper blade size","battery size","p0420","p0300","p0171","p0455","p0442","check engine light","brakes squeaking","car shakes when braking","grinding noise when braking","car shaking when accelerating","car jerks when accelerating","car ac not blowing cold air","car cranks but wont start","engine ticking noise","alternator replacement cost","catalytic converter replacement cost","brake pad replacement cost","rav4 oil capacity","camry tire pressure","f150 towing capacity","silverado recalls","civic tire size","rav4 mpg","f150 p0455",
"2020 rav4 oil capacity","2018 camry tire pressure","2017 f150 fuse box diagram","2015 silverado p0420","2016 honda civic battery size","2018 camry shakes when braking"]
p=TrendReq(hl="en-US",tz=0,retries=2,backoff_factor=2)
out={}
for i in range(0,len(heads),4):
    b=heads[i:i+4]
    for t in range(3):
        try:
            p.build_payload(["gpts"]+b,timeframe="today 3-m",geo="US")
            d=p.interest_over_time(); g=d["gpts"].mean()
            for k in b: out[k]=round(d[k].mean()/g,4) if g else None
            break
        except Exception as e: print("err",e); time.sleep(20)
    time.sleep(6)
json.dump(out,open("trends.json","w"),indent=1)
for k,v in out.items(): print(k,v)
