"""----------------------------------------------------------------------------------------------------
well come, this is maskiiw, this is a simple project about scrapy library.
    in this project we will crawl all data about all cryptos from coinmarketcap.
        this file is backend side.
----------------------------------------------------------------------------------------------------"""
# import what we need:
import json  # https://pypi-json.readthedocs.io/en/latest/
import scrapy  # https://docs.scrapy.org/en/latest/
# -------------------------------------------------


class crypto_info(scrapy.Spider):
    name = "new"
    start_urls = [
        "https://coinmarketcap.com/new/",
        "https://coinmarketcap.com/most-viewed-pages/",
        "https://coinmarketcap.com/trending-cryptocurrencies/",
        "https://coinmarketcap.com/gainers-losers/",
        "https://coinmarketcap.com/cryptocurrency-category/"
    ]

    def start_requests(self):
        headers = {
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
        }
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
                    crypto_chabge_24hour = row.css("td:nth-child(6) ::text").get()
                    crypto_fully_diluted = row.css("td:nth-child(7) ::text").get()
                    crypto_vulome = row.css("td:nth-child(8) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price,
                        "1hour change": crypto_change_hour,
                        "24hour change": crypto_chabge_24hour,
                        "fully diluted": crypto_fully_diluted,
                        "vulome": crypto_vulome
                    }
                    data_list.append(data)
            with open('newcrypto.json', 'w') as json_file:
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
                    crypto_chabge_24hour = row.css("td:nth-child(6) ::text").get()
                    crypto_fully_diluted = row.css("td:nth-child(7) ::text").get()
                    crypto_vulome = row.css("td:nth-child(8) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price,
                        "1hour change": crypto_change_hour,
                        "24hour change": crypto_chabge_24hour,
                        "fully diluted": crypto_fully_diluted,
                        "vulome": crypto_vulome
                    }
                    data_list.append(data)
            with open('mostviewcrypto.json', 'w') as json_file:
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
                    crypto_chabge_24hour = row.css("td:nth-child(6) ::text").get()
                    crypto_chabge_30day = row.css("td:nth-child(7) ::text").get()
                    crypto_fully_diluted = row.css("td:nth-child(8) ::text").get()
                    crypto_vulome = row.css("td:nth-child(9) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price,
                        "1hour change": crypto_change_hour,
                        "24hour change": crypto_chabge_24hour,
                        "30day": crypto_chabge_30day,
                        "fully diluted": crypto_fully_diluted,
                        "vulome": crypto_vulome
                    }
                    data_list.append(data)
            with open('trendcrypto.json', 'w') as json_file:
                j = json.dumps(data_list, indent=2)
                json_file.write(j)

        elif response.url == "https://coinmarketcap.com/gainers-losers/":
            data_list = []
            for i in range(2, 48):
                rows = response.css(f"table tr:nth-child({i})")
                for row in rows:
                    crypto_name = row.css("td:nth-child(2) ::text").get()
                    crypto_price = row.css("td:nth-child(3) ::text").get()
                    crypto_chabge_24hour = row.css("td:nth-child(4) ::text").get()
                    crypto_vulome = row.css("td:nth-child(5) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price,
                        "24hour change": crypto_chabge_24hour,
                        "vulome": crypto_vulome
                    }
                    data_list.append(data)
            with open('gainandlose.json', 'w') as json_file:
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
                    marketcap = row.css("td:nth-child(5) ::text").get()
                    dominance = row.css("td:nth-child(6) ::text").get()
                    crypto_vulome = row.css("td:nth-child(7) ::text").get()
                    gain_lose_num = row.css("td:nth-child(8) ::text").get()
                    data = {
                        "name": crypto_name,
                        "price": crypto_price_change,
                        "1hour change": crypto_top_gainers,
                        "24hour change": marketcap,
                        "fully diluted": dominance,
                        "vulome": crypto_vulome,
                        "gain_lose_num": gain_lose_num
                    }
                    data_list.append(data)
            with open('coinlist.json', 'w') as json_file:
                j = json.dumps(data_list, indent=2)
                json_file.write(j)
# --------------------------------
