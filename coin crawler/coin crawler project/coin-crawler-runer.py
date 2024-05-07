"""----------------------------------------------------------------------------------------------------
well come, this is maskiiw, this is a simple project about scrapy library.
    in this project we will crawl all data about all cryptos from coinmarketcap.
        this file is web service side.
----------------------------------------------------------------------------------------------------"""
# import what we need:
import os  # https://python.readthedocs.io/en/stable/library/os.html
from flask import Flask, request, Response, render_template  # https://flask.palletsprojects.com/en/3.0.x/
# --------------------------------------------------------------------------------------------------------


class Flask_library:

    app = Flask(__name__)
    app.static_folder = 'static'
    crypto_name = None

    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    def get_crypto_name():
        if request.method == 'POST':
            crypto_names = request.form['crypto_names']
            crypto_name = crypto_names
            if crypto_name == "new crypto":
                os.system("scrapy runspider coins-information.py")
                with open(f"newcrypto.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            elif crypto_name == "most view crypto":
                os.system("scrapy runspider coins-information.py")
                with open(f"mostviewcrypto.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            elif crypto_name == "trend crypto":
                os.system("scrapy runspider coins-information")
                with open(f"trendcrypto.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            elif crypto_name == "gain and lose":
                os.system("scrapy runspider coins-information")
                with open(f"gain and lose.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            elif crypto_name == "coin list":
                os.system("scrapy runspider coins-information")
                with open(f"coinlist.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
            else:
                crypto_names = request.form['crypto_names']
                crypto_name = crypto_names
                os.system(f"python3 coin-info.py {crypto_name}")
                with open(f"{crypto_name}.json", 'r') as f:
                    return Response(response=f.read(), status=200, mimetype="application/json")
        return render_template('index.html')


if __name__ == '__main__':
    Flask_library.app.run(port=5000, host="0.0.0.0", debug=True)
# -----------------------------------
