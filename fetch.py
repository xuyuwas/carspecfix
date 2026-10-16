import json,urllib.request,urllib.parse
def get(u):
    r=urllib.request.Request(u,headers={"Accept":"application/json","User-Agent":"Mozilla/5.0"})
    try: return json.load(urllib.request.urlopen(r,timeout=30))
    except Exception as e: return {"_err":str(e)}
P=[("Toyota","RAV4",2020,"RAV4"),("Toyota","RAV4",2024,"RAV4"),("Toyota","Camry",2022,"Camry"),("Toyota","Camry",2024,"Camry"),
("Honda","CR-V",2022,"CR-V"),("Honda","CR-V",2024,"CR-V"),("Ford","F-150",2021,"F150"),("Ford","F-150",2023,"F150"),
("Honda","Civic",2022,"Civic"),("Chevrolet","Silverado",2022,"Silverado"),("Tesla","Model Y",2023,"Model Y"),
("Chevrolet","Equinox",2022,"Equinox"),("Toyota","Corolla",2022,"Corolla"),("Toyota","Tacoma",2022,"Tacoma"),("Honda","Accord",2022,"Accord")]
out=[]
for mk,md,y,fe in P:
    rec=get(f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={mk}&model={urllib.parse.quote(md)}&modelYear={y}")
    rs=rec.get("results",[]) if isinstance(rec,dict) else []
    vp=get(f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeYear/make/{mk}/modelyear/{y}?format=json")
    vok=any(md.lower().replace("-","") in r["Model_Name"].lower().replace("-","") for r in vp.get("Results",[]))
    menu=get(f"https://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year={y}&make={mk}")
    mi=menu.get("menuItem",[]) if isinstance(menu,dict) else []
    if isinstance(mi,dict): mi=[mi]
    models=[m["value"] for m in mi if fe.lower() in m["value"].lower()][:3]
    cfgs=[]
    for m in models:
        o=get(f"https://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year={y}&make={mk}&model={urllib.parse.quote(m)}")
        it=o.get("menuItem",[]) if isinstance(o,dict) else []
        if isinstance(it,dict): it=[it]
        for c in it[:2]:
            v=get(f"https://www.fueleconomy.gov/ws/rest/vehicle/{c['value']}")
            cfgs.append({"fe_id":c["value"],"model":m,"option":c["text"],"engine_l":v.get("displ"),"cyl":v.get("cylinders"),"trans":v.get("trany"),"drive":v.get("drive"),"mpg_city":v.get("city08"),"mpg_hwy":v.get("highway08"),"mpg_comb":v.get("comb08"),"fuel":v.get("fuelType"),"source":f"https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=1&year1={y}&year2={y}&make={mk}&baseModel={urllib.parse.quote(fe)}","api":f"https://www.fueleconomy.gov/ws/rest/vehicle/{c['value']}"})
    out.append({"slug":f"{y}-{mk}-{md}".lower().replace(" ","-"),"year":y,"make":mk,"model":md,"vpic_confirmed":vok,
      "recalls":[{"campaign":r.get("NHTSACampaignNumber"),"component":r.get("Component"),"date":r.get("ReportReceivedDate"),"summary":(r.get("Summary") or "")[:300]} for r in rs],
      "recalls_source":f"https://www.nhtsa.gov/recalls?nhtsaId=&make={mk}&model={md}&year={y}","fueleconomy":cfgs})
    print(y,mk,md,vok,len(rs),len(cfgs))
json.dump(out,open("spec_api_data.json","w"),indent=1)
