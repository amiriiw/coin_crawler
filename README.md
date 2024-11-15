# Coin Crawler

> A cryptocurrency data scraping and web application built with Flask and Scrapy. This project collects cryptocurrency data from CoinMarketCap and serves it through a Flask-based web application, allowing users to view various crypto trends, newly listed coins, top gainers/losers, and specific coin details.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **New Listings**: Fetches information on newly listed cryptocurrencies.
- **Most Viewed Cryptos**: Displays the most viewed cryptocurrencies on CoinMarketCap.
- **Trending Cryptos**: Shows the trending cryptocurrencies.
- **Top Gainers & Losers**: Lists cryptocurrencies with the largest gains and losses.
- **Single Coin Data**: Provides detailed information about a single cryptocurrency, including price, 24-hour change, volume, and market data.

---

## Installation

To set up this project on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/amiriiw/coin_crawler
   cd coin_crawler
   cd Coin-crawler
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the Flask application**:
   ```bash
   python3 app.py
   ```

The Flask app will start on `http://0.0.0.0:5000`. Visit this URL in your browser to view the application.

---

## Usage

### Web Application

1. **Home Page**: The homepage provides options to view different types of cryptocurrency data.
2. **Submit Requests**: Choose an option from the dropdown menu, or enter the name of a cryptocurrency to fetch specific data.
3. **View Data**: The application renders the results in HTML based on the option selected.

### Command-Line Usage

- Run the `all_coins.py` script to scrape various crypto data categories:
  ```bash
  python3 backend/all_coins.py <option>
  ```
  Replace `<option>` with one of the following:
  - `new_crypto`
  - `most_view_crypto`
  - `trend_crypto`
  - `gain_and_lose`
  - `coin_list`

- Run `single_coin.py` for specific cryptocurrency data:
  ```bash
  python3 backend/single_coin.py <crypto_name>
  ```
  Replace `<crypto_name>` with the name of the cryptocurrency, e.g., `bitcoin`.

---

## File Structure

```plaintext
Coin-crawler/
├── app.py                       # Main Flask application
├── requirements.txt             # Dependencies
├── backend/
│   ├── all_coins.py             # Script to scrape various crypto data categories
│   └── single_coin.py           # Script to scrape data for a specific cryptocurrency
├── templates/
│   ├── index.html               # Main page template
│   ├── <other_templates>.html   # Templates for rendering scraped data
└── static/                      # Static assets (CSS, JS)
```

---

## Dependencies

The project relies on the following Python libraries:

- **[Flask](https://flask.palletsprojects.com/)**: Web framework for creating the frontend and API endpoints.
- **[Scrapy](https://scrapy.org/)**: Web scraping framework to gather cryptocurrency data.
- **[requests](https://docs.python-requests.org/)**: HTTP library for handling API requests.
- **[scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)**: Used for rendering JavaScript-heavy web pages during scraping.

Install these dependencies by running:
```bash
pip3 install -r requirements.txt
```

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
