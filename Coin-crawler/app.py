"""code by amiriiw"""
import os
import json
from typing import cast
from flask import Flask, request, Response, render_template


class FlaskLibrary:
    """FlaskLibrary is a class that sets up a Flask application with routes for cryptocurrency data handling."""

    app = Flask(__name__)
    app.static_folder = 'static'

    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    def get_crypto_name() -> Response:
        """Handles GET/POST requests, runs the appropriate script based on user option or crypto name, loads data from JSON and renders the respective HTML."""
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

            user_option = crypto_mapping.get(str(options))
            if user_option:
                return FlaskLibrary.handle_script_execution(user_option)

            return FlaskLibrary.handle_single_coin_request(str(crypto_names))

        return cast(Response, render_template('index.html'))

    @staticmethod
    def handle_script_execution(user_option: str) -> Response:
        """Executes the script based on the user option, loads data from the corresponding JSON file, and renders the HTML."""
        try:
            os.system(f"python3 backend/all_coins.py {user_option}")
            return FlaskLibrary.load_json_and_render_template(user_option)
        except Exception as e:
            return Response(f"An error occurred while executing the script: {str(e)}", status=500)

    @staticmethod
    def handle_single_coin_request(crypto_names: str) -> Response:
        """Handles requests for a single cryptocurrency by executing the relevant script and loading its JSON data."""
        try:
            os.system(f"python3 backend/single_coin.py {crypto_names}")
            return FlaskLibrary.load_json_and_render_template(crypto_names)
        except Exception as e:
            return Response(f"An error occurred while handling the single coin request: {str(e)}", status=500)

    @staticmethod
    def load_json_and_render_template(filename: str) -> Response:
        """Loads JSON data from a file and renders the appropriate HTML template."""
        try:
            with open(f"{filename}.json", 'r') as f:
                data = json.load(f)
            template_name = f'{filename}.html' if filename in {'new_crypto', 'most_view_crypto', 'trend_crypto', 'gain_and_lose', 'coin_list'} else "single_crawl_result.html"
            print(template_name)
            return cast(Response, render_template(template_name, data=data))
        except FileNotFoundError:
            return Response("invalid coin name.", status=404, mimetype="text/plain")
        except json.JSONDecodeError:
            return Response("Error decoding JSON.", status=500, mimetype="text/plain")
        except Exception as e:
            return Response(f"An error occurred while loading JSON: {str(e)}", status=500)


if __name__ == '__main__':
    """Starts the Flask app on port 5000 with debug mode enabled."""
    FlaskLibrary.app.run(port=5000, host="0.0.0.0", debug=True)
