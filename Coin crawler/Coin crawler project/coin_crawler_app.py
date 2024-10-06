# code by amiriiw
import os  
from flask import Flask, request, Response, render_template, json 


class FlaskLibrary:
    app = Flask(__name__)
    app.static_folder = 'static'

    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    def get_crypto_name():
        """ Handles GET/POST requests,  Runs the appropriate script based on user option or crypto name, Loads data from JSON and renders the respective HTML. """
        
        if request.method == 'POST':
            options = request.form.get('options')
            crypto_names = request.form.get('coin_name')
            crypto_mapping = {
                "new crypto": "new_crypto",
                "most view crypto": "most_view_crypto",
                "trend crypto": "trend_crypto",
                "gain and lose": "gain_and_lose",
                "coin list": "coin_list"
            }
            user_option = crypto_mapping.get(options)
            if user_option:
                os.system(f"python3 backend/coin_crawler_all_coins.py {user_option}")
                try:
                    with open(f"{user_option}.json", 'r') as f:
                        data = json.load(f)
                    return render_template(f'{user_option}.html', data=data)
                except FileNotFoundError:
                    return Response("File not found.", status=404, mimetype="text/plain")
            else:
                os.system(f"python3 backend/coin_crawler_single_coin.py {crypto_names}")
                if os.path.isfile(f"{crypto_names}.json"):
                    try:
                        with open(f"{crypto_names}.json", 'r') as f:
                            data = json.load(f)
                        return render_template('single_crawl_result.html', data=data)
                    except FileNotFoundError:
                        return Response("File not found.", status=404, mimetype="text/plain")
                else:
                    with open("invalid_coin_name.json", 'r') as f:
                        return Response(response=f.read(), status=200, mimetype="application/json")
        return render_template('index.html')


if __name__ == '__main__':
    """Starts the Flask app on port 5000 with debug mode enabled."""

    FlaskLibrary.app.run(port=5000, host="0.0.0.0", debug=True)
