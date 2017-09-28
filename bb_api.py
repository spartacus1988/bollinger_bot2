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
        self.prices = {}

        self.url_crypto_compare = None
        self.url_bitTrex_currencies = None
        self.url_coinMarketCup = None


    def build_url_coinMarketCup(self):
        self.url_coinMarketCup = "https://api.coinmarketcap.com/v1/ticker/"

    def build_url_bitTrex_currencies(self):
        self.url_bitTrex_currencies = "https://bittrex.com/api/v1.1/public/getcurrencies"


    def build_url_crypto_compare(self, first, second, totime):
        self.url_crypto_compare = "https://min-api.cryptocompare.com/data/histominute?fsym=" + first + "&tsym=" + second + "&toTs=" + totime + "&limit=20&e=BitTrex"


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

    def extract_crypto_compare(self):
        for item in self.json_crypto_compare["Data"]:
            if item['close'] is not None:
                price = item['close']
                time_st = item['time']
                self.prices[time_st] = price
        self.prices = sorted(self.prices.items())
        #print(self.prices)
        return self.prices




    def merge_coins(self):
        self.btx_currencies = set(self.btx_currencies)
        #print(self.btx_currencies)
        #print(len(self.btx_currencies))

        self.cmc_currencies = set (self.cmc_currencies)
        #print(self.cmc_currencies)
        #print(len(self.cmc_currencies))

        self.merged_currencies = self.btx_currencies.intersection(self.cmc_currencies)
        #print(self.merged_currencies)
        print(len(self.merged_currencies))
        self.merged_currencies = list(self.merged_currencies)
        print(self.merged_currencies)
        print(len(self.merged_currencies))


    def write_coins(self, path_to_coins):
        f = open(path_to_coins, 'w')
        f.writelines("%s\n" % i for i in self.merged_currencies)
        f.close()


    def read_coins(self, path_to_coins):
        with open(path_to_coins, 'r') as f:
            self.merged_currencies = f.read().splitlines()
            print(self.merged_currencies)
            print(len(self.merged_currencies))


def main():
    pass
    api = bb_api()
    #api.build_url_crypto_compare('BTC','USD')

    # api.build_url_bitTrex_currencies()
    #
    #
    # api.json_bitTrex_currencies = api.request(api.url_bitTrex_currencies)
    # api.extract_bitTrex_coins()
    #
    #
    # api.build_url_coinMarketCup()
    # api.json_coinMarketCup = api.request(api.url_coinMarketCup)
    # api.extract_coinMarketCu_coins()
    #
    # api.merge_coins()
    #
    # api.write_coins('all_coins.txt')
    api.read_coins('all_coins.txt')

    api.build_url_crypto_compare('BTC', 'USD', '1506380625')
    api.json_crypto_compare = api.request(api.url_crypto_compare)
    print(jsn.dumps(api.json_crypto_compare, sort_keys=True, indent=4))

    temp_result = api.extract_crypto_compare()
    print(temp_result)






if __name__ == "__main__":
    main()