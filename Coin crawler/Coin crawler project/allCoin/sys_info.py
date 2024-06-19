"""----------------------------------------------------------------------------------------------------
well come, this is maskiiw, this is a simple info about my browser.
    in this file we will collect all info we need in this crawler.
----------------------------------------------------------------------------------------------------"""


class Headers:

    @staticmethod
    def web_headers():
        headers = {
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',

            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        return headers

    @staticmethod
    def post_payload():
        payload = {"mode": "LATEST", "page": 1, "size": 7, "language": "en", "coins": [1], "newsTypes": ["NEWS", "ALEXANDRIA"]}
        return payload
# ---------------------
