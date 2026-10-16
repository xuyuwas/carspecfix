import json,csv,os,urllib.request,urllib.parse,time
UA={'User-Agent':'carspecfix-research/1.0'}
d=json.load(open('picked.json'));idx={r['title']:r for l in d.values() for r in l}
SEL=[
('2020-toyota-rav4','2020 Toyota Rav4 XLE, Front Left, 09-30-2020.jpg','Title/description: "2020 Toyota Rav4 XLE"; category Toyota RAV4 (XA50)','Photographed in Ontario, Canada; XLE is a US/Canada North American trim. Front 3/4.'),
('2024-toyota-rav4','2024 Toyota RAV4 Hybrid Woodland Edition, front right, 03-21-2026.jpg','Description: "2024 Toyota RAV4 Hybrid Woodland Edition" photographed in New Castle, PA; categories 2024 Toyota automobiles, RAV4 Hybrid (XA50)','HYBRID variant (Woodland Edition), not gas-only; same XA50 body. Photographed in USA.'),
('2022-toyota-camry','2022 Toyota Camry SE Standard Package in Celestial Silver Metallic, Front Left, 08-06-2022.jpg','Description: "2022 Toyota Camry SE"; category Toyota Camry (XV70, North America, 2021)','Gas SE; photographed in Ontario, Canada (North American spec).'),
('2022-toyota-camry','2022 Toyota Camry Hybrid XLE in Midnight Black Metallic, Front Right, 12-25-2021.jpg','Description: "2022 Toyota Camry Hybrid XLE ... Assembled in Georgetown, Kentucky"; category XV70 North America 2021','Backup; hybrid variant.'),
('2024-toyota-camry','2024 Toyota Camry Las Vegas Fall 2025.jpg','Description: "A 2024 Toyota Camry at Las Vegas Motor Speedway"; category Toyota Camry (XV70, North America, 2021)','Shot at a racetrack event (USA); check visually for event decals/crowd before use; year claim is uploader-only.'),
('2024-toyota-camry','2023 Toyota Camry XSE, front right, 08-30-2026.jpg','Description says 2023 Camry XSE (USA). NOT 2024: same XV70 North America facelift body as 2024 (unchanged 2021-2024)','SAME-GENERATION SUBSTITUTE, model year differs; caption must not say 2024.'),
('2022-toyota-corolla','2021 Toyota Corolla LE, front right, 07-13-2024.jpg','Description: 2021 Corolla LE, New Castle PA; category Toyota Corolla (E210, North America) sedan. NOT 2022: 2020-2022 US sedan share the pre-2023-refresh body','SAME-GENERATION SUBSTITUTE (2021 MY). No license-valid US 2022 Corolla sedan photo found.'),
('2022-toyota-tacoma','2023 Toyota Tacoma TRD Off-Road Double Cab in Black, front left.jpg','Description: 2023 Tacoma TRD Off-Road, built in Guanajuato MX; category Toyota Tacoma (N300). NOT 2022: same 3rd gen post-2020 facelift (2020-2023)','SAME-GENERATION SUBSTITUTE (2023 MY). License CC BY-SA 3.0 (dual GFDL).'),
('2022-toyota-tacoma','2021 Toyota Tacoma V6 4x4.jpg','Title says 2021; category 2021 Toyota trucks, Tacoma (N300). Same 2020-2023 facelift','Backup substitute; location unknown, uploader description is just "Toyota Tacoma".'),
('2022-honda-cr-v','2022 Honda CR-V EX-L (facelift), front 3.31.23.jpg','Description: "A 2022 Honda CR-V EX-L facelift photographed in Flushing, Queens, NY"; category CR-V 5th gen','Photographed in USA.'),
('2024-honda-cr-v','Honda CR-V EX-L AWD (2024) (53625033461).jpg','Title "(2024)"; Flickr description: Sixth generation, 1.5L petrol, CVT, AWD; category United States photographs taken on 2024-03-29','Gas 1.5T EX-L, matches the signed gas-only page. Flickr import reviewed by FlickreviewR.'),
('2024-honda-cr-v','2023 Honda CR-V EX-L AWD, front right, 11-13-2022.jpg','Description 2023 CR-V EX-L AWD, New Castle PA; 6th gen same as 2024','Backup; SAME-GENERATION SUBSTITUTE (2023 MY).'),
('2022-honda-civic','2022 Honda Civic LX Sedan, front right, 11-02-2022.jpg','Description: "2022 Honda Civic LX Sedan photographed in New Castle, Pennsylvania"; category Honda Civic (2021) sedan','Photographed in USA.'),
('2022-honda-accord','2022 Honda Accord Sport in Sonic Grey Pearl, Front Left, 01-30-2022.jpg','Description: "2022 Honda Accord Sport"; category Honda Accord (2017)','Photographed in Ontario, Canada (North American spec).'),
('2021-ford-f-150','2021 Ford F-150 SuperCrew, front 4.28.21.jpg','Description: "A 2021 Ford F-150 SuperCrew photographed in Queens, NY"; category 14th gen, 2021 Ford trucks','Photographed in USA.'),
('2023-ford-f-150','2023 Ford F-150 SuperCrew Pick-Up (52810350195).jpg','Title "2023 Ford F-150 SuperCrew"; Twin Cities Auto Show, Minneapolis, April 2023; category 14th gen','Auto-show shot (background/stands may appear). Flickr import, license reviewed by FlickreviewR.'),
('2022-chevrolet-silverado-1500','2022 Chevrolet Silverado 1500 LT in Summit White, Front Left, 06-26-2022.jpg','Description "2022 Chevrolet Silverado 1500 LT"; category Silverado (GMTT1XX)','2022 had two versions (carryover "LTD" and refreshed 2022). Image shows one of them; confirm which visually vs. our spec data. Photographed in Ontario, Canada.'),
('2022-chevrolet-silverado-1500','2022 Chevrolet Silverado K1500 LT-L, front 4.24.23.jpg','Description "A 2022 Chevrolet Silverado K1500" photographed in Manorville, NY','Backup, USA. Same 2022 LTD/refresh caveat.'),
('2022-chevrolet-equinox','2022 Chevrolet Equinox LT (facelift), front 6.2.22.jpg','Description "A 2022 Chevrolet Equinox LT facelift photographed in Flushing, Queens, NY"; 3rd gen','Photographed in USA; 2022 is the facelift year, matches.'),
('2023-tesla-model-y','2023 Tesla Model Y, front 11.11.23.jpg','Description "A 2023 Tesla Model Y Long Range photographed in Flushing, Queens, NY"','Photographed in USA. Model Y page data itself still unsigned.'),
]
rows=[]
for slug,f,ev,note in SEL:
    r=idx['File:'+f];os.makedirs(slug,exist_ok=True)
    fn=os.path.splitext(f)[0].replace(' ','_').replace(',','')[:80]+'.jpg';path=f'{slug}/{fn}'
    if not os.path.exists(path):
        for i in range(3):
            try: open(path,'wb').write(urllib.request.urlopen(urllib.request.Request(r['thumb'],headers=UA),timeout=60).read());break
            except Exception as e: print('retry',e);time.sleep(5)
    t=f.rsplit('.',1)[0]
    rows.append(dict(slug=slug,file=path,commons_page_url=r['page'],author=r['artist'],license=r['lic'],license_url=r['licurl'],
     required_attribution_text=f'Photo: "{t}" by {r["artist"]}, via Wikimedia Commons, {r["lic"]} ({r["licurl"]})'+(' — resized' ),
     model_year_evidence=ev,notes=note+' Downloaded as 1920px-wide Commons thumbnail.'+(' Share-alike: derivatives of the image must stay under same license.' if 'SA' in r['lic'] else '')))
rows.append(dict(slug='(none missing)',file='',commons_page_url='',author='',license='',license_url='',required_attribution_text='',model_year_evidence='',notes='All 14 slugs have at least one candidate; 2024 Camry, 2022 Corolla, 2022 Tacoma rely on same-generation adjacent-year photos (see notes).'))
w=csv.DictWriter(open('image_sources.csv','w',newline=''),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
