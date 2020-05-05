import hashlib
import hmac
import json
import time
import urllib
import requests


API_KEY = "your api key here"
API_SECRET = "your api secret here"

BITMEX_URL = "https://www.bitmex.com"


def main():
    # example : buy 100 qty at price 5000 USD
    # bitmex_limit_order('Buy',5000,100)
    bitmex_mywallet()
    # show your wallet status


def bitmex_limit_order(action, price , quantity):
    verb = 'POST'
    path = '/api/v1/order?symbol=XBTUSD&side=' + action + '&orderQty=' + str(quantity) + '&price=' + str(price) + '&ordType=Limit'
    expires = int(time.time()) + 10
    signature = bitmex_signature(API_SECRET, verb, path, expires)
    header = {'api-expires' : str(expires) , 'api-key' : API_KEY, 'api-signature' : signature}
    order_run = requests.post(BITMEX_URL + path , data='' , headers = header)
    print(order_run.content)


def bitmex_mywallet():
    verb = 'GET'
    path = "/api/v1/user/wallet?currency=XBt"
    expires = int(time.time()) + 10
    signature = bitmex_signature(API_SECRET, verb, path, expires)
    header = {'api-expires' : str(expires) , 'api-key' : API_KEY, 'api-signature' : signature}
    wallet_run = urllib.request.Request(BITMEX_URL + path , headers = header)
    data = urllib.request.urlopen(wallet_run).read()
    print(data)


def bitmex_signature(apiSecret, verb, url, nonce, postdict=None):
    data = ''
    if postdict:
        data = json.dumps(postdict, separators=(',', ':'))
    parsedURL = urllib.parse.urlparse(url)
    path = parsedURL.path
    if parsedURL.query:
        path = path + '?' + parsedURL.query
    message = (verb + path + str(nonce) + data).encode('utf-8')
    signature = hmac.new(apiSecret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
    return signature


if __name__ == "__main__":
    main()
