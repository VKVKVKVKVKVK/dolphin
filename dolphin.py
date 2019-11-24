from apiCalls import *
from optimize import *
from utils import *

#Contraintes du portefeuille:
# - 15 actifs distincts minimum & 40 maximum
# - Au moins 50% d'actions
# - % NAV d'un actif du portefeuille doit être compris entre 1% et 10% à la date du 14/06/2013
# - Le portefeuille n'aura qu'une unique composition commençant le 14/06/2013
# - Evaluation du sharpe du 14/06/2013 au 18/04/2019 (Modification du sujet, cf. mail)
# - 10/20 attribué automatiquement si ratio de sharpe supérieur strictement au portefeuille naif


#Print pf sharpes
oursharpes = post_ratio([12], [1835])
refsharpes = post_ratio([12], [2201])
print("Our sharpes: " + str(json.loads(oursharpes.content.decode('utf-8'))))
print("Ref sharpes: " + str(json.loads(refsharpes.content.decode('utf-8'))))

#Call Get All Assets
print("Fetching all assets in database...")
assets = getAssetsCache()
print("Total number of Assets in Database: " + str(len(assets)) + "\n")

printBestSharpes(assets)


#Printing REF portfolio ...
#print("Printing ref Portfolio...")
#ref = get_portfolio(2201)
#refjson = json.loads(ref.content.decode('utf-8'))
#print(json.dumps(refjson, indent=4, sort_keys=True))

assetinfos = getAssetInfos(assets)
#assets_by_id = {}

testoptimizedpfgenerator(assets, assetinfos)
exit(0) ################################ IT MAY EXITS HERE ######################################## <------------

#FIXME: portfolios have been removed from variable "assets" -> get it with api
#FIXME: save only REF in file (ours may change)
#Getting our portfolios
print("Getting our portfolios...")
main_portfolios = {}
#if os.path.exists("json/main_portfolios.json"):
#    with open('json/main_portfolios.json') as json_file:
#        main_portfolios = json.load(json_file)
#else:
#    main_portfolios = get_start_portfolio(assets)
#    with open('json/main_portfolios.json', 'w+') as json_file:
#        json.dump(main_portfolios, json_file, indent=4, sort_keys=True)

ref_portfolio = {}
own_portfolio = {}
if os.path.exists("json/ref_portfolio.json"):
    with open('json/ref_portfolio.json') as json_file:
        ref_portfolio = json.load(json_file)
else:
    ref_portfolio = json.loads(get_asset_by_id(2201).content.decode('utf-8'))
    with open('json/ref_portfolio.json', 'w') as json_file:
        json.dump(ref_portfolio, json_file, indent=4, sort_keys=True)
own_portfolio = json.loads(get_asset_by_id(1835).content.decode('utf-8'))
with open('json/ref_portfolio.json', 'w') as json_file:
    json.dump(own_portfolio, json_file, indent=4, sort_keys=True)

#Variables for Epita and Reference portfolios
#epita = main_portfolios[0]
#ref = main_portfolios[1]

#main_portfolios = get_start_portfolio(assets)
#for i in main_portfolios:
#    print("ID : " + i['ASSET_DATABASE_ID']['value'] + ", Label : " + i['LABEL']['value'])
#print('\n')
print("ID : " + ref_portfolio['ASSET_DATABASE_ID']['value'] + ", Label : " + ref_portfolio['LABEL']['value'])
print("ID : " + own_portfolio['ASSET_DATABASE_ID']['value'] + ", Label : " + own_portfolio['LABEL']['value'])


for i in assetinfos:
    print("Label ID: " + str(i.get_id()) + ", Currency: " + i.get_currency() + ", Quotation: " + str(i.get_quotation()))

#Veryfing out updated portfolio
print("Printing our updated portfolio...")
#ref = get_portfolio(1835)
#refjson = json.loads(ref.content.decode('utf-8'))
#print(json.dumps(refjson, indent=4, sort_keys=True))
print(json.dumps(own_portfolio, indent=4, sort_keys=True))
#FIXME volumes peuvent pas etre en float
