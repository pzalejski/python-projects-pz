
import time
from datetime import datetime
from requests import ConnectionError, Timeout, TooManyRedirects
import json
import requests

from config import email, password, pnum, api_key

from sms import bitcoin_sms, email_login, em, pas, sms_gateway
import sms

url = 'https://pro-api.coinmarketcap.com/v1/'\
        'cryptocurrency/quotes/latest?symbol=BTC&convert=USD'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
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


def format_bitcoin_sms(bitcoin_price):
  rows = []
  for coin_price in bitcoin_price:
    #Formats the date into a string: '24.02.2018 15:09'
    date = coin_price['date'].strftime('%b %d,%Y %H:%M')
    price = coin_price['price']
    row = f"{date}:     {price}"
    rows.append(row)
  return '\n'.join(rows)

def main():
  email_login(em, pas)
  bitcoin_price = []
  i = 0
  while i<5:
    price = get_latest_btc_price()
    date = datetime.now()
    bitcoin_price.append({'date': date, 'price': price})
    i += 1
    #getting prices with 5 min intervals (60*5)
    #for testing purposes, using 10s intervals
    time.sleep(5)
  body = format_bitcoin_sms(bitcoin_price)
  bitcoin_sms(em, sms_gateway, 'Latest Bitcoin Prices:', body)
  



if __name__ == "__main__":
    main()
