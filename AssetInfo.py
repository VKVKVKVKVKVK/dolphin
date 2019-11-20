class AssetInfo:
    def __init__(self, id = -1, quotation = -1, volume = -1, currency = -1):
        self.id = id
        self.quotation = quotation
        self.volume = volume
        self.currency = "EUR" #convert(currency, "EUR", quotation) if quotation != -1 else quotation
    #FIXME: en fait osef des getters :D, ça a l'air d'être public par défaut
    def get_id(self):
        return self.id

    def set_id(self, x):
        self.id = x

    def get_quotation(self):
        return self.quotation

    def set_quotation(self, x):
        self.quotation = x

    def get_currency(self):
        return self.currency

    def set_currency(self, x):
        self.currency = x

    def get_volume(self):
        return self.volume

    def set_volume(self, x):
        self.volume = x