import requests
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from collections import namedtuple

#Contraintes du portefeuille:
# - 15 actifs distincts minimum & 40 maximum
# - Au moins 50% d'actions
# - % NAV d'un actif du portefeuille doit être compris entre 1% et 10% à la date du 14/06/2013
# - Le portefeuille n'aura qu'une unique composition commençant le 14/06/2013
# - Evaluation du sharpe du 14/06/2013 au 18/04/2019 (Modification du sujet, cf. mail)
# - 10/20 attribué automatiquement si ratio de sharpe supérieur strictement au portefeuille naif

#FIXME: change hardcoded dates partout
STARTDATE = "2013-06-14"
ENDDATE = "2019-04-19"


#INFORMATIONS DE LOG AU SERVEUR
URL = 'https://dolphin.jump-technology.com:8443/api/v1'
AUTH =('EPITA_GROUPE16', 'n3ky4D6cwmVe5Zax')
#username: EPITA_GROUPE16
#password: n3ky4D6cwmVe5Zax

#https: // dolphin.jump - technology.com: 8443 / api / v1 / asset / 1792


#portefeuilleyolo:
defpf = [2201, 2142 ,2143 , 2132, 2188, 2112, 1990, 2064, 2144, 2187, 1968, 2191, 2147, 1897, 1877]
#1-9: 10%
#10-15: 10/6
THUNES = 100000 #FIXME

def columns_to_str(columns):
    return "/".join(columns)

def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


#Récupère infos sur un asset en particulier (id passé en paramètre)
def get_asset_by_id(id, date=None, full_response=False, columns=list()):
    endpointApi = "/asset/" + str(id)
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns)
    print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#Récupère liste de tout les assets avec ID, Label, Type et Cotation à la date spécifiée (harcodée 2013-06-14 ici)
def get_assets(date=None, full_response=True, columns=list()):
    endpointApi = "/asset"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + "?columns=ASSET_DATABASE_ID" + "&columns=LABEL" \
           + "&columns=TYPE" + "&columns=LAST_CLOSE_VALUE_IN_CURR" + "&date=2013-06-14"
    #print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#Récupère cotation sur un asset en particulier (id passé en paramètre) pour dates hardcodées FIXME CHECK LA DATE
def get_asset_quotation_by_id(id, date=None, full_response=False, columns=list()):
    endpointApi = "/asset/" + str(id) + "/quote"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + "?start_date=2013-06-14&end_date=2019-04-19"
    print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#Récupère les ratios existants
def get_ratios(date=None, full_response=False, columns=list()):
    endpointApi = "/ratio/"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns)
    print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res


#Récupère la  composition d'un portefeuille
def get_portfolio(portfolio_id, date=None, full_response=False, columns=list()):
    endpointApi = "/portfolio/"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + str(portfolio_id) + "/dyn_amount_compo"
    print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#Set la  composition d'un portefeuille
def set_portfolio(portfolio_id, assets, date=None, full_response=False, columns=list()):
    endpointApi = "/portfolio/"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + str(portfolio_id) + "/dyn_amount_compo"
    print(path)
    params = {
        'label' : 'EPITA_PTF_16',
        'currency' : {
            "code": "€"
        },
        'type' : 'front',
        'values' : {
            STARTDATE : []
        }
    }
    for i in assets:
        params['values'][STARTDATE].append(
            {
                "asset": {
                    "asset": i['id'],
                    "quantity": i['quantity']
                }
            }
        )
    res = requests.put(path,
                       data=json.dumps(params),
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#sharpe: 12
def post_ratio(ratio, assets, date=None, full_response=False, columns=list()):
    endpointApi = "/ratio/invoke/"
    payload = {'date': date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns)
    params = {
        'ratio': ratio,
        'asset': assets,
        'start_date': '2013-06-14',
        'end_date': '2019-04-19'
    }
    res = requests.post(path,data=json.dumps(params),auth=AUTH,verify=False)
    return res

#Call Get All Assets
res_assets = get_assets()
assets = json.loads(res_assets.content.decode('utf-8'))
print("Total number of Assets in Database: " + str(len(assets)) + "\n")
#for i in e:
#    print(i)

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

print("\n".join(str(v[0]) for v in sortedratios))

ref = get_portfolio(2201)
refjson = json.loads(ref.content.decode('utf-8'))
#print(refjson)
print(json.dumps(refjson, indent=4, sort_keys=True))

assets = []
assetsvalues = [] #FIXME: les récupérer
c = 0
for i in defpf:
    #bob le bricoleur
    val = THUNES * 10/100 if c < 9 else THUNES * (10 / 6) / 100
    qu = val #FIXME: virer ça
    #qu = val / assetsvalues[c] #FIXME: décommenter ça
    assets.append(
        {
            'id' : i,
            'quantity' : qu
        }
    )
    c += 1

res = set_portfolio(1835, assets)
print(json.loads(res.content.decode('utf-8')))
#samarchpa: error 500 sans message d'erreur :D

#bruteforce les ids ma bite
#for id in range(1000):
#    print("id: " + str(id))
#    ref = get_portfolio(id)
#    print(json.loads(ref.content.decode('utf-8')))
#    if(ref.ok):
#        tmp = raw_input("nice");

#print(sortedratios[0:30])


""" 
#Call Get Asset by Id
asset = get_asset_by_id(URL,"/asset/1875")
d = json.loads(asset.content.decode('utf-8'))
for key, value in d.items():
    print(key, value)
print(d["LABEL"]["value"])

#Call Get Asset Quotation by Id
asset_quote = get_asset_quotation_by_id(URL,"/asset/1875/quote")
f = json.loads(asset_quote.content.decode('utf-8'))
for i in f:
    print(i)

#Call Get Ratios
ratios = get_ratios(URL,"/ratio")
r = json.loads(ratios.content.decode('utf-8'))
for i in r:
    print(i)

#Call Get Portfolio
portfolio = get_portfolio(URL,"/portfolio/", 10)
p = json.loads(portfolio.content.decode('utf-8'))
for i in p:
    print(i)

#Nombre d'actifs dans portefeuille (initialisé à 0)
asset_number = 0

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

y = json2obj(data)

print(y.name, y.hometown.name, y.hometown.id)

"""