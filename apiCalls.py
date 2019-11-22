from vars import *

def convert(input_currency, value):
    call = convert_currency(input_currency)
    answer = json.loads(call.content.decode('utf-8'))
    temp = answer['rate']['value']
    #Convert string to list for converting to correct format: "x,xxx" => "x.xxx"
    listvalues = list(temp)
    for n, i in enumerate(listvalues):
        if i == ",":
            listvalues[n] = "."
    final = "".join(listvalues)
    return float(final)*float(value)


def convert_currency(input, date=None, full_response=True, columns=list()):
    endpointApi = "/currency/rate/"
    payload = {'date': date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + input + "/to/" \
           + "EUR" + "?date=2013-06-14"
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

def columns_to_str(columns):
    return "/".join(columns)

#def _json_object_hook(d):
#    return namedtuple('X', d.keys())(*d.values())

#def json2obj(data):
#    return json.loads(data, object_hook=_json_object_hook)


#R�cup�re infos sur un asset en particulier (id pass� en param�tre)
def get_asset_by_id(id, date=None, full_response=False, columns=list()):
    endpointApi = "/asset/" + str(id)
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns)
    #print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#R�cup�re liste de tout les assets avec ID, Label, Type et Cotation � la date sp�cifi�e (harcod�e 2013-06-14 ici)
def get_assets(date=None, full_response=True, columns=list()):
    endpointApi = "/asset"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + "?columns=ASSET_DATABASE_ID" + "&columns=LABEL" \
           + "&columns=TYPE" + "&columns=LAST_CLOSE_VALUE_IN_CURR" + "&columns=IS_PORTFOLIO" + "&date=2013-06-14"
    #print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#R�cup�re cotation sur un asset en particulier (id pass� en param�tre) pour dates hardcod�es FIXME CHECK LA DATE
def get_asset_quotation_by_id(id, date=None, full_response=False, columns=list()): #FIXME je crois que t'avais modif un truc (la p�riode)
    endpointApi = "/asset/" + str(id) + "/quote"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + "?start_date=2013-06-14&end_date=2019-04-19"
    #print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#R�cup�re les ratios existants
def get_ratios(date=None, full_response=False, columns=list()):
    endpointApi = "/ratio/"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns)
    #print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

def get_start_portfolio(assets):
    start = []
    for i in assets:
        if i['TYPE']['value'] == 'PORTFOLIO':
            start.append(i)
    return start

#R�cup�re la  composition d'un portefeuille
def get_portfolio(portfolio_id, date=None, full_response=False, columns=list()):
    endpointApi = "/portfolio/"
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + str(portfolio_id) + "/dyn_amount_compo"
    #print(path)
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
            "code": "EUR" #FIXME maybe switch to EUR/� ?
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

#Build portfolio based on volume constraints
def buildnaifpf(assets, assetsratios):
    res = []
    missing = 0 #FIXME: adjust with remaining CAPITAL?
    i = 0
    for a in assets :
        val = CAPITAL * assetsratios[i] + missing
        if val > CAPITAL / 10:
            print("ERROR: > 10% for id: " + str(assets[i].id) + ", adjusting...\n")
            missing = val - CAPITAL / 10
            val = CAPITAL / 10
        wqu = val / assets[i].quotation
        diff = wqu - assets[i].volume
        if diff > 0:
            print("ERROR: not enough assets for id: " + str(assets[i].id) + ", adjusting...\n")
            missing += diff * assets[i].quotation
            qu = assets[i].volume
        else:
            qu = wqu
        diffint = qu - int(qu)
        if diffint != 0:
            print("WARNING: quantity is not an integer for id: " + str(assets[i].id) + ", adjusting...") 
            missing += diffint * assets[i].quotation
        res.append(
            {
                'id' : a.id,
                'quantity' : qu
            }
        )
        i += 1
    return res
