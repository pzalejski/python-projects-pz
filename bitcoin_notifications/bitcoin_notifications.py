
import time
from datetime import datetime
from pip._vendor.requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pip._vendor.requests
import config
# def main():
#     pass

# if __name__ == "__main__":
#     main()

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC&convert=USD'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': config.api_key,
}
r = pip._vendor.requests.request("GET",url, headers=headers)
if r.status_code == 200:
    response = json.loads(r.text)
print(response)