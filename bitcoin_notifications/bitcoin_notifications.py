
import time
from datetime import datetime
from requests import ConnectionError, Timeout, TooManyRedirects
import json
import requests
import config
# def main():
#     pass

# if __name__ == "__main__":
#     main()

url = 'https://pro-api.coinmarketcap.com/v1/'\
        'cryptocurrency/quotes/latest?symbol=BTC&convert=USD'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': config.api_key,
}
r = requests.request("GET", url, headers=headers)
if r.status_code == 200:
    response = json.loads(r.text)
print(response)
