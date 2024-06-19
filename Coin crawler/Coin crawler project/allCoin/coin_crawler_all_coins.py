"""----------------------------------------------------------------------------------------------------
well come, this is maskiiw, this is a simple project about scrapy crawler.
    in this project we will crawl all data about all cryptos from coinmarketcap.
        this file is backend side.
----------------------------------------------------------------------------------------------------"""
# import what we need:
import os  # https://python.readthedocs.io/en/stable/library/os.html
import time  # https://docs.python.org/3/library/time.html
import json  # https://pypi-json.readthedocs.io/en/latest/
import scrapy  # https://docs.scrapy.org/en/latest/
from sys_info import Headers  # me
from scrapy.crawler import CrawlerProcess  # https://docs.scrapy.org/en/latest/
# -----------------------------------------------------------------------------


class CryptoInfo(scrapy.Spider):

    name = "new"
    start_urls = [
        "https://coinmarketcap.com/new/",
        "https://coinmarketcap.com/most-viewed-pages/",
        "https://coinmarketcap.com/trending-cryptocurrencies/",
        "https://coinmarketcap.com/gainers-losers/",
        "https://coinmarketcap.com/cryptocurrency-category/"
    ]

    def start_requests(self):
        headers = Headers.web_headers()
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response, **kwargs):
        if response.url == "https://coinmarketcap.com/new/":
            data_list = []
            for i in range(2, 32):
                rows = response.css(f"table tr:nth-child({i})")
                for row in rows:
                    crypto_name = row.css("td:nth-child(3) ::text").get()
                    crypto_price = row.css("td:nth-child(4) ::text").get()
                    crypto_change_hour = row.css("td:nth-child(5) ::text").get()
                    crypto_change_24hour = row.css("td:nth-child(6) ::text").get()
                    crypto_fully_diluted = row.css("td:nth-child(7) ::text").get()
                    crypto_volume = row.css("td:nth-child(8) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price,
                        "1hour change": crypto_change_hour,
                        "24hour change": crypto_change_24hour,
                        "fully diluted": crypto_fully_diluted,
                        "volume": crypto_volume
                    }
                    data_list.append(data)
            with open('new_crypto.json', 'w') as json_file:
                j = json.dumps(data_list, indent=2)
                json_file.write(j)

        elif response.url == "https://coinmarketcap.com/most-viewed-pages/":
            data_list = []
            for i in range(2, 32):
                rows = response.css(f"table tr:nth-child({i})")
                for row in rows:
                    crypto_name = row.css("td:nth-child(3) ::text").get()
                    crypto_price = row.css("td:nth-child(4) ::text").get()
                    crypto_change_hour = row.css("td:nth-child(5) ::text").get()
                    crypto_change_24hour = row.css("td:nth-child(6) ::text").get()
                    crypto_fully_diluted = row.css("td:nth-child(7) ::text").get()
                    crypto_volume = row.css("td:nth-child(8) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price,
                        "1hour change": crypto_change_hour,
                        "24hour change": crypto_change_24hour,
                        "fully diluted": crypto_fully_diluted,
                        "volume": crypto_volume
                    }
                    data_list.append(data)
            with open('most_view_crypto.json', 'w') as json_file:
                j = json.dumps(data_list, indent=2)
                json_file.write(j)

        elif response.url == "https://coinmarketcap.com/trending-cryptocurrencies/":
            data_list = []
            for i in range(2, 32):
                rows = response.css(f"table tr:nth-child({i})")
                for row in rows:
                    crypto_name = row.css("td:nth-child(3) ::text").get()
                    crypto_price = row.css("td:nth-child(4) ::text").get()
                    crypto_change_hour = row.css("td:nth-child(5) ::text").get()
                    crypto_change_24hour = row.css("td:nth-child(6) ::text").get()
                    crypto_change_30day = row.css("td:nth-child(7) ::text").get()
                    crypto_fully_diluted = row.css("td:nth-child(8) ::text").get()
                    crypto_volume = row.css("td:nth-child(9) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price,
                        "1hour change": crypto_change_hour,
                        "24hour change": crypto_change_24hour,
                        "30day": crypto_change_30day,
                        "fully diluted": crypto_fully_diluted,
                        "volume": crypto_volume
                    }
                    data_list.append(data)
            with open('trend_crypto.json', 'w') as json_file:
                j = json.dumps(data_list, indent=2)
                json_file.write(j)

        elif response.url == "https://coinmarketcap.com/gainers-losers/":
            data_list = []
            for i in range(2, 48):
                rows = response.css(f"table tr:nth-child({i})")
                for row in rows:
                    crypto_name = row.css("td:nth-child(2) ::text").get()
                    crypto_price = row.css("td:nth-child(3) ::text").get()
                    crypto_change_24hour = row.css("td:nth-child(4) ::text").get()
                    crypto_volume = row.css("td:nth-child(5) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price,
                        "24hour change": crypto_change_24hour,
                        "volume": crypto_volume
                    }
                    data_list.append(data)
            with open('gain_and_lose.json', 'w') as json_file:
                j = json.dumps(data_list, indent=2)
                json_file.write(j)

        elif response.url == "https://coinmarketcap.com/cryptocurrency-category/":
            data_list = []
            for i in range(2, 32):
                rows = response.css(f"table tr:nth-child({i})")
                for row in rows:
                    crypto_name = row.css("td:nth-child(2) ::text").get()
                    crypto_price_change = row.css("td:nth-child(3) ::text").get()
                    crypto_top_gainers = row.css("td:nth-child(4) ::text").get()
                    crypto_change_24hour = row.css("td:nth-child(5) ::text").get()
                    dominance = row.css("td:nth-child(6) ::text").get()
                    crypto_volume = row.css("td:nth-child(7) ::text").get()
                    gain_lose_num = row.css("td:nth-child(8) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price_change,
                        "1hour change": crypto_top_gainers,
                        "24hour change": crypto_change_24hour,
                        "fully diluted": dominance,
                        "volume": crypto_volume,
                        "gain_lose_num": gain_lose_num
                    }
                    data_list.append(data)
            with open('coin_list.json', 'w') as json_file:
                j = json.dumps(data_list, indent=2)
                json_file.write(j)

    @staticmethod
    def main():
        process = CrawlerProcess()
        process.crawl(CryptoInfo), process.start()


if __name__ == "__main__":
    path = "new_crypto.json"
    if os.path.isfile(path):
        if time.time() - os.path.getmtime(path) <= 60:
            exit()

    crypto_info_spider = CryptoInfo()
    crypto_info_spider.main()
# ---------------------------
