import json as jsn
import requests


class bb_api:

    def __init__(self):
        self.json = None
        self.json_crypto_compare = None
        self.json_bitTrex_currencies = None
        self.json_coinMarketCup = None

        self.btx_currencies = []
        self.cmc_currencies = []
        self.merged_currencies = set()

        self.url_crypto_compare = None
        self.url_bitTrex_currencies = None
        self.url_coinMarketCup = None


    def build_url_coinMarketCup(self):
        self.url_coinMarketCup = "https://api.coinmarketcap.com/v1/ticker/"

    def build_url_bitTrex_currencies(self):
        self.url_bitTrex_currencies = "https://bittrex.com/api/v1.1/public/getcurrencies"


    def build_url_crypto_compare(self, first, second):
        self.url_crypto_compare = "https://min-api.cryptocompare.com/data/histominute?fsym=" + first + "&tsym=" + second + "&limit=1&e=BitTrex"


    def request(self, url):
        self.json = requests.get(url).text
        #print(self.json)
        self.json = jsn.loads(self.json)
        #print(jsn.dumps(self.json, sort_keys=True, indent=4))
        return self.json

    def extract_bitTrex_coins(self):
        #print(self.json_bitTrex_currencies["result"][1]["Currency"])
        for currency in self.json_bitTrex_currencies["result"]:
            if(currency["IsActive"] == True):
                self.btx_currencies.append(currency["Currency"])
        print(self.btx_currencies)

    def extract_coinMarketCu_coins(self):
        #print(self.json_coinMarketCup[0]['market_cap_usd'])
        for currency in self.json_coinMarketCup:
            if currency['market_cap_usd'] is not None and currency['24h_volume_usd'] is not None:
                if(float(currency['market_cap_usd']) > 50000000) or (float(currency['24h_volume_usd']) > 200000):
                    self.cmc_currencies.append(currency["symbol"])
        print(self.cmc_currencies)

    def merge_coins(self):
        self.btx_currencies = set(self.btx_currencies)
        print(self.btx_currencies)
        print(len(self.btx_currencies))

        self.cmc_currencies = set (self.cmc_currencies)
        print(self.cmc_currencies)
        print(len(self.cmc_currencies))

        self.merged_currencies = self.btx_currencies.intersection(self.cmc_currencies)
        print(self.merged_currencies)
        print(len(self.merged_currencies))
        self.merged_currencies = list(self.merged_currencies)
        print(self.merged_currencies)



def main():
    pass
    api = bb_api()
    #api.build_url_crypto_compare('BTC','USD')

    api.build_url_bitTrex_currencies()


    api.json_bitTrex_currencies = api.request(api.url_bitTrex_currencies)
    api.extract_bitTrex_coins()


    api.build_url_coinMarketCup()
    api.json_coinMarketCup = api.request(api.url_coinMarketCup)
    api.extract_coinMarketCu_coins()

    api.merge_coins()







if __name__ == "__main__":
    main()