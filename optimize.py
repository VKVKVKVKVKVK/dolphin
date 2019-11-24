from apiCalls import *

#volatilit�: 10
def optimize(assets, power):

    #If value found, cast in float, otherwise, write "nofloatdata"
    def pairid_floatval(p, val):
        try:
            return (int(p[0]), float(p[1][val]['value'].replace(",", ".")))
        except:
            return ("nofloatdata", 0)

    #Store array of all ids
    ids = [a['ASSET_DATABASE_ID']['value'] for a in assets]

                ############ VOLATILITIES ############
    #get volatilities (ratio number 10 to call on API) values on all assets
    ret_volatilities = json.loads(post_ratio([10], ids).content.decode('utf-8'))
    #Create dictionnary with ids and volatilities
    volatilities = dict(map(lambda p: pairid_floatval(p,'10') , ret_volatilities.items()))
    #Remove assets with no data for volatility
    volatilities = dict(filter(lambda p: p[0] != "nofloatdata", volatilities.items()))

                ############ SHARPE ############

    #get sharpe ratios
    ret_sratios = json.loads(post_ratio([12], ids).content.decode('utf-8'))
    #Create dictionnary with id and sharpes value
    sharpes = dict(map(lambda p: pairid_floatval(p,'12') , ret_sratios.items()))
    #remove no data items
    sratios = dict(filter(lambda p: p[0] != "nofloatdata", sharpes.items()))
    #compute new ratios (sharpe/volatility)
    newratios = dict()
    for r in sratios.items():
        newratios[r[0]] = (r[1] * volatilities[r[0]]) / (volatilities[r[0]]**power)

    #Sort them
    final = sorted(newratios.items(), key = lambda p: p[1], reverse=True)

    #get ids for best values and return the first 15 values
    best_values = [f[0] for f in final]
    n = 22
    top_n = best_values[:n]
    return top_n, newratios

#Building portfolio with CAPITAL constraints
def testoptimizedpfgenerator(assets, infos):
    #Get 15 best values according to our function
    bestassets, customsharpes = optimize(assets, 0.6)
    tmpinfos = []
    #for y in bestassets[:15]:
    #    tmpinfos.append(AssetInfo(y, 1, 1000000, "EUR"))
    for a in bestassets:
        for i in infos:
            if a == i.id:
                tmpinfos.append(i)
    #for t in tmpinfos:
    #    res = post_ratio([12], [t.get_id()])
    #    sharpe = json.loads(res.content.decode('utf-8'))
    #    print("Id: " + str(t.get_id()) + ", Sharpe: " + str(sharpe))
    ratios = []
    ratios.append(0.1)
    for i in range(1, len(tmpinfos)):
        ratios.append(customsharpes[tmpinfos[i].id] / customsharpes[tmpinfos[i-1].id] * ratios[-1])
        if ratios[-1] < 0:
            print("WARNING: RATIO  < 1")
        #FIXME(oupa): not all checks done
    pf = buildnaifpf(tmpinfos, ratios) #[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1/6,0.1/6,0.1/6,0.1/6,0.1/6,0.1/6])
    set_portfolio(1835, pf)
    set_portfolio(1835, pf) #set twice sinon c truc de merde se met pas � jour
    ret = post_ratio([12], [1835])
    print("our yolo sharpes: " + str(json.loads(ret.content.decode('utf-8'))))
    #exit(0)

    #Build portfolio based on volume constraints
def buildnaifpf(assets, assetsratios):
    res = []
    missing = 0 #FIXME: adjust with remaining CAPITAL?
    i = 0
    for a in assets :
        val = CAPITAL * assetsratios[i] # + missing #FIXME: add missing?
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
            qu = int(qu)
        res.append(
            {
                'id' : a.id,
                'quantity' : qu
            }
        )
        i += 1
    return res


#####OBSOLETE#####

def pfbysharpe(assetsinfos):
    assets = []
    assetsvalues = []
    assetsnb = []
    assetsratios = []
    for i in range(9):    
        assetsratios.append(0.1)
    for i in range(6):
        assetsratios.append(0.1/6)
    for i in defpf:
        for a in assetinfos:
            if a.id == i:
                assets.append(a)
                break
        print("ERROR: ID not found\n")

    pf = buildnaifpf(assets, assetsratios)
    res = set_portfolio(1835, pf)
    print(res.status_code) #OK


def printBestSharpes(assets):
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
    try:
        print(", ".join(str(int(v[0])) for v in sortedratios))
    except:
        1;
    print("\n")