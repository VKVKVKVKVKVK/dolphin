import requests
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


URL = 'https://dolphin.jump-technology.com:8443/api/v1'
AUTH =('EPITA_GROUPE16', 'n3ky4D6cwmVe5Zax')
#username: EPITA_GROUPE16
#password: n3ky4D6cwmVe5Zax

#https: // dolphin.jump - technology.com: 8443 / api / v1 / asset / 1792

def columns_to_str(columns):
    return "/".join(columns)

def get_asset_by_id(URL, endpointApi, date=None, full_response=False, columns=list()):
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns)
    print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

def get_assets(URL, endpointApi, date=None, full_response=True, columns=list()):
    payload = {'date':date, 'fullResponse': full_response}
    path = URL + endpointApi + columns_to_str(columns) + "?columns=ASSET_DATABASE_ID" + "&columns=LABEL"
    print(path)
    res = requests.get(path,
                       params=payload,
                       auth=AUTH,
                       verify=False)
    return res

#Call Get Asset by Id
asset = get_asset_by_id(URL,"/asset/1875")

d = json.loads(asset.content.decode('utf-8'))
for key, value in d.items():
    print(key, value)


#Call Get All Assets
assets = get_assets(URL,"/asset")
e = json.loads(assets.content.decode('utf-8'))
print(len(e))
for i in e:
    print(i)



