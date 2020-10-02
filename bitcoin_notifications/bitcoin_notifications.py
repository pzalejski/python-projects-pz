
import time
from datetime import datetime
from requests import ConnectionError, Timeout, TooManyRedirects
import json
import requests
import config

url = 'https://pro-api.coinmarketcap.com/v1/'\
        'cryptocurrency/quotes/latest?symbol=BTC&convert=USD'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': config.api_key,
}
r = requests.request("GET", url, headers=headers)
if r.status_code == 200:
    response = json.loads(r.text)
# print(response)


def get_latest_btc_price():
  response = requests.get(url,headers=headers)
  response_json = response.json()
  #convert the price to a floating point number round to 3 decimals
  return (round(float(response_json['data']['BTC']['quote']['USD']['price']),3))

get_latest_btc_price()


def main():
  bitcoin_price = []
  i = 0
  while i<5:
    price = get_latest_btc_price()
    date = datetime.now()
    bitcoin_price.append({'date': date, 'price': price})
    i += 1
    #getting prices with 5 min intervals
    #for testing purposes, using 10s intervals
    time.sleep(10)
  print(bitcoin_price)



if __name__ == "__main__":
    main()
