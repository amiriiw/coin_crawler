"""----------------------------------------------------------------------------------------------------
well come, this is maskiiw, this is a simple project about scrapy library.
    in this project we will crawl all data about all cryptos from coinmarketcap.
        this file is backend side.
----------------------------------------------------------------------------------------------------"""
# import what we need:
import os  # https://python.readthedocs.io/en/stable/library/os.html
import sys  # https://docs.python.org/3/library/sys.html
import json  # https://pypi-json.readthedocs.io/en/latest/
import time  # https://docs.python.org/3/library/time.html
import scrapy  # https://docs.scrapy.org/en/latest/
import requests  # https://requests.readthedocs.io/en/latest/
from scrapy_splash import SplashRequest  # https://splash.readthedocs.io/en/stable/faq.html
from scrapy.crawler import CrawlerProcess  # https://docs.scrapy.org/en/latest/
# ------------------------------------------------------------------------


class CryptoInfo(scrapy.Spider):

    name = "ghost"
    is_process_done = False

    def __init__(self, crypto_name, *args, **kwargs):
        print(crypto_name)
        super(CryptoInfo, self).__init__(*args, **kwargs)
        super().__init__(**kwargs)
        self.crypto = crypto_name
        self.start_urls = [f"https://coinmarketcap.com/currencies/{crypto}/"]

    def start_requests(self):
        headers = {
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',

            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        for url in self.start_urls:
            yield SplashRequest(url, headers=headers, callback=self.parse, args={"wait": 2})

    def parse(self, response, **kwargs):
        new_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
        }
        post_payload = {"mode": "LATEST", "page": 1, "size": 7, "language": "en", "coins": [1], "newsTypes": ["NEWS", "ALEXANDRIA"]}

        coin_name = (
            response.css("span.sc-d1ede7e3-0.bEFegK ::text").get())
        coin_logo = (
            response.css("div.sc-d1ede7e3-0.bqEaSQ ::attr(class)").get())
        coin_price = (
            response.css("span.sc-d1ede7e3-0.fsQm.base-text ::text").get())
        coin_24hour_change = (
            response.css("p.sc-71024e3e-0.sc-58c82cf9-1.bgxfSG.iPawMI ::text").get())
        coin_lower_price_in_24_hour = (
            response.css("div.sc-d1ede7e3-0.bwRagp.flexBetween > div:nth-child(1) > span ::text").get())
        coin_higher_price_in_24_hour = (
            response.css("div.sc-d1ede7e3-0.bwRagp.tlr span ::text").get())
        coin_all_time_high = (
            response.css("div.sc-d1ede7e3-0.dCkvaR span ::text").get())
        coin_all_time_low = (
            response.css("div:nth-child(4) > div > div.sc-d1ede7e3-0.dCkvaR > span ::text").get())
        about_coin = (
            "".join(response.css("div.sc-d1ede7e3-0.esMjFQ.show div:nth-child(1) ::text").getall()).strip())
        coin_news = (
            requests.post("https://api.coinmarketcap.com/aggr/v4/content/user", post_payload, headers=new_headers).json())

        coin_markets = requests.get(
            f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={self.crypto}&start=1&limit=10&category=spot&centerType=cex&sort=cmc_rank_advanced&direction=desc&spotUntracked=true")
        coin_markets = coin_markets.json()
        coin_markets = coin_markets["data"]["marketPairs"]
        for pair_index in range(len(coin_markets)):
            coin_markets[pair_index] = {
                "rank": coin_markets[pair_index]["rank"],
                "exchangeId": coin_markets[pair_index]["exchangeId"],
                "exchangeName": coin_markets[pair_index]["exchangeName"],
                "marketPair": coin_markets[pair_index]["marketPair"],
                "marketUrl": coin_markets[pair_index]["marketUrl"],
                "baseSymbol": coin_markets[pair_index]["baseSymbol"],
                "price": coin_markets[pair_index]["price"],
                "volumeUsd": coin_markets[pair_index]["volumeUsd"],
                "volumeBase": coin_markets[pair_index]["volumeBase"],
                "volumeQuote": coin_markets[pair_index]["volumeQuote"],
                "volumePercent": coin_markets[pair_index]["volumePercent"],
                "type": coin_markets[pair_index]["type"],
                "quotes": coin_markets[pair_index]["quotes"]
            }

        crypto_id = (
            response.css("div.sc-f70bb44c-0.iQEJet.BaseChip_labelWrapper__lZ4ii ::text").get())
        coin_analytics_data = requests.get(
            f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/info/get-analytics?cryptoId={crypto_id}&timeRangeType=month1")
        coin_analytics_data = coin_analytics_data.json()
        data = {
            "name": coin_name,
            "logo": coin_logo,
            "price": coin_price,
            "24hour change": coin_24hour_change,
            "lower price in 24 hour": coin_lower_price_in_24_hour,
            "higher price in 24 hour": coin_higher_price_in_24_hour,
            "all time-high": coin_all_time_high,
            "all time-low": coin_all_time_low,
            "about coin": about_coin,
            "markets": coin_markets,
            "analytics": coin_analytics_data,
            "news": coin_news,
        }
        with open(f'{crypto}.json', 'w') as json_file:
            j = json.dumps(data, indent=2)
            json_file.write(j)
            CryptoInfo.is_process_done = True
        return j
    if not is_process_done:
        message = "invalid crypto name!"
        with open(f'invalid_coin_name.json', 'w') as json_file:
            j = json.dumps(message, indent=2)
            json_file.write(j)

    def main(self):
        process = CrawlerProcess()
        process.crawl(CryptoInfo, self.crypto), process.start()


if __name__ == "__main__":
    crypto = sys.argv[1]
    path = f"{crypto}.json"
    if os.path.isfile(path):
        if time.time() - os.path.getmtime(path) <= 60:
            exit()
    crypto_info_spider = CryptoInfo(crypto)
    crypto_info_spider.main()
# ___________________________
