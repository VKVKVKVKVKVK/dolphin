from apiCalls import *

#Contraintes du portefeuille:
# - 15 actifs distincts minimum & 40 maximum
# - Au moins 50% d'actions
# - % NAV d'un actif du portefeuille doit être compris entre 1% et 10% à la date du 14/06/2013
# - Le portefeuille n'aura qu'une unique composition commençant le 14/06/2013
# - Evaluation du sharpe du 14/06/2013 au 18/04/2019 (Modification du sujet, cf. mail)
# - 10/20 attribué automatiquement si ratio de sharpe supérieur strictement au portefeuille naif

#volatilité: 10
def optimize(assets, power):
    def crotedebic(p, val):
        try:
            return (int(p[0]), float(p[1][val]['value'].replace(",", ".")))
        except:
            return ("tamer", 0)
    ids = [a['ASSET_DATABASE_ID']['value'] for a in assets]
    ret_volatilities = json.loads(post_ratio([10], ids).content.decode('utf-8'))
    troll = dict(map(lambda p: crotedebic(p,'10') , ret_volatilities.items()))
    volatilities = dict(filter(lambda prout: prout[0] != "tamer", troll.items()))    
    ret_sratios = json.loads(post_ratio([12], ids).content.decode('utf-8'))
    troll = dict(map(lambda p: crotedebic(p,'12') , ret_sratios.items()))
    sratios = dict(filter(lambda prout: prout[0] != "tamer", troll.items()))
    newratios = dict()
    for r in sratios.items():
        newratios[r[0]] = r[1] / (volatilities[r[0]]**power)
    final = sorted(newratios.items(), key = lambda p: p[1], reverse=True)
    chingching = [f[0] for f in final]
    chinghing = chingching[:15]
    return chingching

oursharpes = post_ratio([12], [1835])
refsharpes = post_ratio([12], [2201])
print("our sharpes: " + str(json.loads(oursharpes.content.decode('utf-8'))))
print("ref sharpes: " + str(json.loads(refsharpes.content.decode('utf-8'))))

#Call Get All Assets
print("Fetching all assets in database...")
assets = {}
if os.path.exists("json/assets.json"):
    with open('json/assets.json') as json_file:
        assets = json.load(json_file)
else:
    res_assets = get_assets()
    assets = json.loads(res_assets.content.decode('utf-8'))
    with open('json/assets.json', 'w+') as json_file:
        json.dump(assets, json_file, indent=4, sort_keys=True)

print("Total number of Assets in Database: " + str(len(assets)) + "\n")

def testnico():
    yolo = optimize(assets, 1)
    yololo = []
    for y in yolo[:15]:
        yololo.append(AssetInfo(y, 1, 1000000, "EUR"))
    yolopf = buildnaifpf(yololo, [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1/6,0.1/6,0.1/6,0.1/6,0.1/6,0.1/6])
    set_portfolio(1835, yolopf)
    yoloret = post_ratio([12], [1835])
    print("our yolo sharpes: " + str(json.loads(yoloret.content.decode('utf-8'))))
    #FIXME: hum, c'est bien comme ça qu'on récupère le ratio de sharpe du portefeuille? paske la valeur ne change pas avec le nb portefeuille
    exit(0)
#testnico()

#Getting our portfolios
print("Getting our portfolios...")
main_portfolios = {}
if os.path.exists("json/main_portfolios.json"):
    with open('json/main_portfolios.json') as json_file:
        main_portfolios = json.load(json_file)
else:
    main_portfolios = get_start_portfolio(assets)
    with open('json/main_portfolios.json', 'w+') as json_file:
        json.dump(main_portfolios, json_file, indent=4, sort_keys=True)


#main_portfolios = get_start_portfolio(assets)
for i in main_portfolios:
    print("ID : " + i['ASSET_DATABASE_ID']['value'] + ", Label : " + i['LABEL']['value'])
print('\n')


#Variables for Epita and Reference portfolios
epita = main_portfolios[0]
ref = main_portfolios[1]


assetsids = [o['ASSET_DATABASE_ID']['value'] for o in assets]
res_ratios = post_ratio([12], assetsids)
#temp = json.loads(ratio.content.decode('utf-8'))
#print(temp)
ratios = json.loads(res_ratios.content.decode('utf-8'))
for i in assetsids:
    ratios[i] = ratios[i]['12']['value']
#ratios = for r in ratios:
 #   r
sortedratios = sorted(ratios.items(), key=lambda kv: kv[1], reverse=True)
sortedratios = sortedratios[0:40]

print("ID's with best Sharpe ratio: ")
print(", ".join(str(v[0]) for v in sortedratios))
print("\n")


#Printing REF portfolio ...
#print("Printing ref Portfolio...")
ref = get_portfolio(2201)
refjson = json.loads(ref.content.decode('utf-8'))
#print(json.dumps(refjson, indent=4, sort_keys=True))

assetinfos = []
copy_assets = assets
#assets_by_id = {}

for i in copy_assets:
    if i["ASSET_DATABASE_ID"]["value"] == "1835" or i["ASSET_DATABASE_ID"]["value"] == "2201" :
        continue
    assetinfos.append(AssetInfo(i["ASSET_DATABASE_ID"]["value"]))

    """ 
    if os.path.exists("json/assets_by_id.json"):
        with open('json/assets_by_id.json') as json_file:
            assets_by_id = json.load(json_file)
        for j in assets_by_id:
            if j["ASSET_DATABASE_ID"]["value"] == i["ASSET_DATABASE_ID"]["value"]:
                
    else:
        main_portfolios = get_start_portfolio(assets)
        with open('json/main_portfolios.json', 'w+') as json_file:
            json.dump(main_portfolios, json_file, indent=4, sort_keys=True)
    
    """
    assetres = get_asset_by_id(assetinfos[-1].get_id())
    asset = json.loads(assetres.content.decode('utf-8'))
    print(asset["ASSET_DATABASE_ID"]["value"])
    assetinfos[-1].set_currency(asset["CURRENCY"]["value"])

    quoteres = get_asset_quotation_by_id(assetinfos[-1].get_id())
    quote = json.loads(quoteres.content.decode('utf-8'))
    if len(quote) == 0:
        continue
    #print(json.dumps(quote, indent=4, sort_keys=True))
    assetinfos[-1].set_quotation(quote[0]["close"]["value"])
    #assetinfos[-1].set_volume(quote[0]["volume"]["value"])
    #FIXME: get volume

for i in assetinfos:
    print("Label ID: " + str(i.get_id()) + ", Currency: " + i.get_currency() + ", Quotation: " + str(i.get_quotation()))

assets = []
########### Remove when assets getter is fine
assetsvalues = []
assetsnb = []
assetsratios = []
for i  in range(15):
    assets.append(AssetInfo(defpf[i], 1, 100000, 'EUR'))
for i in range(9):    
    assetsratios.append(0.1)
for i in range(6):
    assetsratios.append(0.1/6)
###########
for i in defpf:
    for a in assetinfos:
        if a.id == i:
            assets.append(a)
            break
    print("ERROR: ID not found\n")

pf = buildnaifpf(assets, assetsratios)
res = set_portfolio(1835, pf)
print(res.status_code) #OK

#Veryfing out updated portfolio
print("Printing our updated portfolio...")
ref = get_portfolio(1835)
refjson = json.loads(ref.content.decode('utf-8'))
print(json.dumps(refjson, indent=4, sort_keys=True))
#FIXME volumes peuvent pas etre en float
