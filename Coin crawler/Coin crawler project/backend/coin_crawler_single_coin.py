# code by amiriiw
import os  
import sys  
import json  
import time  
import scrapy  
import requests 
from scrapy_splash import SplashRequest 
from scrapy.crawler import CrawlerProcess 


class CryptoInfo(scrapy.Spider):
    name = "ghost"
    is_process_done = False

    def __init__(self, crypto_name, *args, **kwargs):
        """ Initializes the spider with the crypto name and sets start URLs. """

        super().__init__(*args, **kwargs)
        self.crypto = crypto_name
        self.start_urls = [f"https://coinmarketcap.com/currencies/{self.crypto}/"]

    def start_requests(self):
        """ Sends initial requests with custom headers via Splash for JavaScript handling. """

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.5'}
        for url in self.start_urls:
            yield SplashRequest(url, headers=headers, callback=self.parse, args={"wait": 2})

    def parse(self, response, **kwargs):
        """ Extracts crypto data from the page and external APIs, then saves it as JSON. """

        coin_name = response.css(
            "#section-coin-overview div:nth-child(1) h1:nth-child(2) span ::text").get()
        coin_logo = response.css(
            "#section-coin-overview div:nth-child(1) div img ::attr(src)").get()
        coin_price = response.css(
            "#section-coin-overview > div:nth-child(2) span ::text").get()
        coin_24hour_change = response.css(
            "#section-coin-overview div:nth-child(2) div div p ::text").get()
        coin_lower_price_in_24_hour = response.css(
            "#__next div:nth-child(2) section:nth-child(2) > div > div:nth-child(4) div:nth-child(2) div:nth-child(1) span ::text").get()
        coin_higher_price_in_24_hour = response.css(
            "#__next section:nth-child(2) div:nth-child(4) div:nth-child(2) div:nth-child(2) span ::text").get()
        coin_all_time_high = response.css(
            "#__next section:nth-child(2) div:nth-child(4) div:nth-child(3) div:nth-child(2) span ::text").get()
        coin_all_time_low = response.css(
            "#__next section:nth-child(2) div:nth-child(4) div:nth-child(4) div:nth-child(2) span ::text").get()
        about_coin = "".join(response.css(
            "#section-coin-about section div:nth-child(1) div:nth-child(2) div div ::text").getall()).strip()
        coin_news = requests.post(
            "https://api.coinmarketcap.com/aggr/v4/content/user").json()
        coin_markets_response = requests.get(
            f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={self.crypto}&start=1&limit=10&category=spot&centerType=cex&sort=cmc_rank_advanced&direction=desc&spotUntracked=true")
        coin_markets = coin_markets_response.json().get("data", {}).get("marketPairs", [])

        coin_markets_data = [
            {
                "rank": market["rank"],
                "exchangeId": market["exchangeId"],
                "exchangeName": market["exchangeName"],
                "marketPair": market["marketPair"],
                "marketUrl": market["marketUrl"],
                "baseSymbol": market["baseSymbol"],
                "price": market["price"],
                "volumeUsd": market["volumeUsd"],
                "volumeBase": market["volumeBase"],
                "volumeQuote": market["volumeQuote"],
                "volumePercent": market["volumePercent"],
                "type": market["type"],
                "quotes": market["quotes"]
            }
            for market in coin_markets
        ]
        crypto_id = response.css("div.sc-f70bb44c-0.iQEJet.BaseChip_labelWrapper__lZ4ii ::text").get()
        coin_analytics_data_response = requests.get(
            f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/info/get-analytics?cryptoId={crypto_id}&timeRangeType=month1")
        coin_analytics_data = coin_analytics_data_response.json()
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
            "markets": coin_markets_data,
            "analytics": coin_analytics_data,
            "news": coin_news,
        }

        with open(f'{self.crypto}.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
            CryptoInfo.is_process_done = True

    @staticmethod
    def handle_invalid_crypto_name():
        """ Saves an error message for invalid crypto names. """

        message = "invalid crypto name!"
        with open('invalid_coin_name.json', 'w') as json_file:
            json.dump(message, json_file, indent=2)

    def main(self):
        """ Starts the scrapy crawler. """

        process = CrawlerProcess()
        process.crawl(CryptoInfo, self.crypto)
        process.start()


if __name__ == "__main__":
    """ Checks if the data is recent, if not, initiates the crawl. """

    crypto = sys.argv[1]
    path = f"{crypto}.json"
    if os.path.isfile(path) and time.time() - os.path.getmtime(path) <= 30:
        sys.exit()
    crypto_info_spider = CryptoInfo(crypto)
    crypto_info_spider.main()
