import requests
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from collections import namedtuple
from AssetInfo import AssetInfo
import pandas as pd
import pickle
import time

#FIXME: change hardcoded dates partout
STARTDATE = "2013-06-14"
ENDDATE = "2019-04-19"


#INFORMATIONS DE LOG AU SERVEUR
URL = 'https://dolphin.jump-technology.com:8443/api/v1'
AUTH =('EPITA_GROUPE16', 'n3ky4D6cwmVe5Zax')
#username: EPITA_GROUPE16
#password: n3ky4D6cwmVe5Zax

#https: // dolphin.jump - technology.com: 8443 / api / v1 / asset / 1792


#portefeuille avec les 15 assets avec le plus haut ratio de sharpes:
defpf = [2201, 2142 ,2143 , 2132, 2188, 2112, 1990, 2064, 2144, 2187, 1968, 2191, 2147, 1897, 1877]
#1-9: 10%
#10-15: 10/6
CAPITAL = 1000000 #1000000

currencyvalues = {
    "EUR" : 1,
    "TEST" : 1.5
}
