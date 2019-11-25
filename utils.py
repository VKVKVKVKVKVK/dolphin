from apiCalls import *


#Get assets
def getAssetsCache():
    assets = {}
    if os.path.exists("json/assets.json"):
        with open('json/assets.json') as json_file:
            assets = json.load(json_file)
    else:
        res_assets = get_assets()
        assets = json.loads(res_assets.content.decode('utf-8'))

        output_dict = [x for x in assets if x['IS_PORTFOLIO']['value'] == 'false']


        with open('json/assets.json', 'w+') as json_file:
            json.dump(output_dict, json_file, indent=4, sort_keys=True)
    return assets


#Get assets as AssetInfos
def getAssetInfos(assets):
    assetinfos = []
    if os.path.exists("assetinfos.dmp"):
        assetinfosfile = open("assetinfos.dmp", "rb")
        assetinfos = pickle.load(assetinfosfile)
        assetinfosfile.close()
    else:    
        for i in assets:
            if i["ASSET_DATABASE_ID"]["value"] == "1835" or i["ASSET_DATABASE_ID"]["value"] == "2201" :
                continue
            assetinfos.append(AssetInfo(int(i["ASSET_DATABASE_ID"]["value"])))
            assetres = get_asset_by_id(assetinfos[-1].get_id())
            asset = json.loads(assetres.content.decode('utf-8'))
            print(asset["ASSET_DATABASE_ID"]["value"])
            assetinfos[-1].set_currency(asset["CURRENCY"]["value"])

            quoteres = get_asset_quotation_by_id(assetinfos[-1].get_id())
            quote = json.loads(quoteres.content.decode('utf-8'))
            if len(quote) == 0:
                continue
            #print(json.dumps(quote, indent=4, sort_keys=True))
            assetinfos[-1].set_quotation(convert(asset["CURRENCY"]["value"], quote[0]["close"]["value"]))
            #assetinfos[-1].set_volume(quote[0]["volume"]["value"])
            #FIXME: get volume
        assetinfosfile = open("assetinfos.dmp", "wb")
        pickle.dump(assetinfos, assetinfosfile)
        assetinfosfile.close()
    return assetinfos