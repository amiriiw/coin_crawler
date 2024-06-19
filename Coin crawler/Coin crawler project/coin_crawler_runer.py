"""----------------------------------------------------------------------------------------------------
well come, this is maskiiw, this is a simple project about scrapy crawler.
    in this project we will crawl all data about all cryptos from coinmarketcap.
        this file is web service side.
----------------------------------------------------------------------------------------------------"""
# import what we need:
import os  # https://python.readthedocs.io/en/stable/library/os.html
from flask import Flask, request, Response, render_template  # https://flask.palletsprojects.com/en/3.0.x/
# --------------------------------------------------------------------------------------------------------


class FlaskLibrary:

    app = Flask(__name__)
    app.static_folder = 'static'
    crypto_name = None

    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    def get_crypto_name():
        if request.method == 'POST':
            crypto_names = request.form['crypto_names']

            if crypto_names == "new crypto":
                os.system("python3 allCoin/coin_crawler_all_coins.py")
                with open(f"new_crypto.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            elif crypto_names == "most view crypto":
                os.system("python3 allCoin/coin_crawler_all_coins.py")
                with open(f"most_view_crypto.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            elif crypto_names == "trend crypto":
                os.system("python3 allCoin/coin_crawler_all_coins.py")
                with open(f"trend_crypto.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            elif crypto_names == "gain and lose":
                os.system("python3 allCoin/coin_crawler_all_coins.py")
                with open(f"gain_and_lose.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            elif crypto_names == "coin list":
                os.system("python3 allCoin/coin_crawler_all_coins.py")
                with open(f"coin_list.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            else:
                crypto_names = request.form['crypto_names']
                os.system(f"python3 singleCoin/coin_crawler_single_coin.py {crypto_names}")
                if os.path.isfile(f"{crypto_names}.json"):
                    with open(f"{crypto_names}.json", 'r') as f:
                        return Response(response=f.read(), status=200, mimetype="application/json")
                else:
                    with open("invalid_coin_name.json", 'r') as f:
                        return Response(response=f.read(), status=200, mimetype="application/json")
        return render_template('index.html')


if __name__ == '__main__':
    FlaskLibrary.app.run(port=5000, host="0.0.0.0", debug=True)
# --------------------------------------------------------------
