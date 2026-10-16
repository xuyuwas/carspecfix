import json,re,csv
s=json.load(open("suggest.json")); y=json.load(open("suggest_ymm.json"))
bad=re.compile(r"belouizdad|zamalek|satisfaction|airport|amtrak|animal|shelter|menu|abc store|golf|park|arena|access portal|civic action|civic activities|civic ai|qatar|bike|quest 2|ac unit|albany|near me|tooth|quanto|club car|mattress|lincoln town|restaurant|hotel|weather|mall|beach|news|police|hospital|school|tacoma wa|county|apartments|jobs")
car=re.compile(r"\b(oil|tire|tyre|wiper|battery|fuse|recall|tow|mpg|mileage|p0\d\d\d|code|brake|shak|jerk|grind|noise|smell|start|crank|engine|ac |a/c|light|cost|replace|filter|spark|transmission|problem|sensor|alternator|catalytic|rav|camry|cr v|cr-v|crv|f150|f 150|civic|corolla|silverado|accord|tacoma|model y|accelerat|squeak|tick|burning|cold air|evap|misfire|lean|leak)")
seen={};
for seed,l in s.items():
    for k in l:
        if not bad.search(k) and car.search(k): seen.setdefault(k,("autosuggest",seed))
for q,l in y.items():
    for k in l:
        if not bad.search(k): seen.setdefault(k,("autosuggest_ymm",q))
w=csv.writer(open("keywords.csv","w",newline=""))
for k in sorted(seen): w.writerow([k])
json.dump(seen,open("kw_meta.json","w"))
print(len(seen))
import collections
c=collections.Counter(v[1] for v in seen.values()); print(c.most_common())
