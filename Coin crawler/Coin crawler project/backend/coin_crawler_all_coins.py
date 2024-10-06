# code by amiriiw
import os  
import sys 
import time  
import json  
import scrapy  
from scrapy.crawler import CrawlerProcess 


class CryptoInfo(scrapy.Spider):
    name = "ghost"

    def __init__(self, position_, *args, **kwargs):
        """ Initializes the spider with the given crypto position. """
        
        print(position_)
        super().__init__(*args, **kwargs)
        self.position = position_
        self.start_urls = self.get_start_urls()

    def get_start_urls(self):
        """ Returns the start URLs based on the crypto position. """
        
        position_to_url = {
            "new_crypto": "https://coinmarketcap.com/new/",
            "most_view_crypto": "https://coinmarketcap.com/most-viewed-pages/",
            "trend_crypto": "https://coinmarketcap.com/trending-cryptocurrencies/",
            "gain_and_lose": "https://coinmarketcap.com/gainers-losers/",
            "coin_list": "https://coinmarketcap.com"
        }
        return [position_to_url.get(self.position)] if self.position in position_to_url else []

    def start_requests(self):
        """ Sends requests to the start URLs with custom headers. """

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.5'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response, **kwargs):
        """ Selects the appropriate parser based on the crypto position. """

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
        """ Parses the 'new crypto' page. """

        return self.parse_table(response, range(1, 32), [
            "name", "price", "1hour change", "24hour change",
            "fully diluted", "volume"
        ])

    def parse_most_view_crypto(self, response):
        """ Parses the 'most viewed crypto' page. """

        return self.parse_table(response, range(1, 32), [
            "name", "price", "24hour change", "1week change",
            "1month change", "marketcap"
        ])

    def parse_trend_crypto(self, response):
        """ Parses the 'trending crypto' page. """

        return self.parse_table(response, range(1, 32), [
            "name", "price", "24hour change", "1week change",
            "30day", "marketcap", "volume"
        ])

    def parse_gain_and_lose(self, response):
        """ Parses the 'gainers and losers' page. """

        return self.parse_table(response, range(1, 48), [
            "name", "price", "24hour change", "volume"
        ])

    def parse_coin_list(self, response):
        """ Parses the 'coin list' page. """

        return self.parse_table(response, range(1, 32), [
            "name", "price", "1hour change", "24hour change",
            "1month change", "gain_lose_num", "volume"
        ])

    def parse_table(self, response, row_range, fields):
        """ Parses table data from the page. """

        data_list = []
        for i in row_range:
            row = response.css(f"table tr:nth-child({i})")
            if position == "gain_and_lose":
                data = {field: row.css(f"td:nth-child({index+2}) ::text").get() for index, field in enumerate(fields)}
            else:
                data = {field: row.css(f"td:nth-child({index+3}) ::text").get() for index, field in enumerate(fields)}
            data_list.append(data)
        return data_list

    @staticmethod
    def save_to_json(data_list, file_name=None):
        """ Saves the data to a JSON file. """

        if not file_name:
            file_name = f"{sys.argv[1]}.json"
        with open(file_name, 'w') as json_file:
            json.dump(data_list, json_file, indent=2)

    @staticmethod
    def main():
        """ Starts the scrapy crawler. """

        process = CrawlerProcess()
        position_arg = sys.argv[1]
        process.crawl(CryptoInfo, position_=position_arg)
        process.start()


if __name__ == "__main__":
    """ Checks if the file is recent; if not, starts the crawl. """

    positions = {
        "new_crypto": "new_crypto.json",
        "most_view_crypto": "most_view_crypto.json",
        "trend_crypto": "trend_crypto.json",
        "gain_and_lose": "gain_and_lose.json",
        "coin_list": "coin_list.json"
    }
    position = sys.argv[1]
    print(position)
    file_path = positions.get(position)
    if file_path and os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) <= 30:
        sys.exit()
    CryptoInfo.main()
