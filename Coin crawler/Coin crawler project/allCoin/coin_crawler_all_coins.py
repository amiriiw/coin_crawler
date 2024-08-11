"""-----------------------------------------------------------------------
well come, this is amiriiw, this is a simple project about scrapy crawler.
    in this project we will crawl all data about all cryptos from coinmarketcap.
        this file is backend side.
-------------------------------"""
import os  # https://python.readthedocs.io/en/stable/library/os.html
import sys  # https://docs.python.org/3/library/sys.html
import time  # https://docs.python.org/3/library/time.html
import json  # https://pypi-json.readthedocs.io/en/latest/
import scrapy  # https://docs.scrapy.org/en/latest/
from sys_info import Headers  # me
from scrapy.crawler import CrawlerProcess  # https://docs.scrapy.org/en/latest/
"""-------------------------------------------------------------------------"""


class CryptoInfo(scrapy.Spider):
    name = "ghost"

    def __init__(self, position_, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = position_
        self.start_urls = self.get_start_urls()

    def get_start_urls(self):
        position_to_url = {
            "new_crypto": "https://coinmarketcap.com/new/",
            "most_view_crypto": "https://coinmarketcap.com/most-viewed-pages/",
            "trend_crypto": "https://coinmarketcap.com/trending-cryptocurrencies/",
            "gain_and_lose": "https://coinmarketcap.com/gainers-losers/",
            "coin_list": "https://coinmarketcap.com/cryptocurrency-category/"
        }
        return [position_to_url.get(self.position)] if self.position in position_to_url else []

    def start_requests(self):
        headers = Headers.web_headers()
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response, **kwargs):
        parsers = {
            "new_crypto": self.parse_new_crypto,
            "most_view_crypto": self.parse_most_view_crypto,
            "trend_crypto": self.parse_trend_crypto,
            "gain_and_lose": self.parse_gain_and_lose,
            "coin_list": self.parse_coin_list
        }
        parser = parsers.get(self.position)
        if parser:
            data_list = parser(response)
            self.save_to_json(data_list)

    def parse_new_crypto(self, response):
        return self.parse_table(response, range(2, 32), [
            "name", "price", "1hour change", "24hour change",
            "fully diluted", "volume"
        ])

    def parse_most_view_crypto(self, response):
        return self.parse_table(response, range(2, 32), [
            "name", "price", "1hour change", "24hour change",
            "fully diluted", "volume"
        ])

    def parse_trend_crypto(self, response):
        return self.parse_table(response, range(2, 32), [
            "name", "price", "1hour change", "24hour change",
            "30day", "fully diluted", "volume"
        ])

    def parse_gain_and_lose(self, response):
        return self.parse_table(response, range(2, 48), [
            "name", "price", "24hour change", "volume"
        ])

    def parse_coin_list(self, response):
        return self.parse_table(response, range(2, 32), [
            "name", "price", "1hour change", "24hour change",
            "fully diluted", "volume", "gain_lose_num"
        ])

    def parse_table(self, response, row_range, fields):
        data_list = []
        for i in row_range:
            row = response.css(f"table tr:nth-child({i})")
            data = {field: row.css(f"td:nth-child({index+2}) ::text").get() for index, field in enumerate(fields)}
            data_list.append(data)
        return data_list

    @staticmethod
    def save_to_json(data_list, file_name=None):
        if not file_name:
            file_name = f"{sys.argv[1]}.json"
        with open(file_name, 'w') as json_file:
            json.dump(data_list, json_file, indent=2)

    @staticmethod
    def main():
        process = CrawlerProcess()
        position_arg = sys.argv[1]
        process.crawl(CryptoInfo, position=position_arg)
        process.start()


if __name__ == "__main__":
    positions = {
        "new_crypto": "new_crypto.json",
        "most_view_crypto": "most_view_crypto.json",
        "trend_crypto": "trend_crypto.json",
        "gain_and_lose": "gain_and_lose.json",
        "coin_list": "coin_list.json"
    }
    position = sys.argv[1]
    file_path = positions.get(position)
    if file_path and os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) <= 30:
        sys.exit()
    CryptoInfo.main()
"""---------------"""
