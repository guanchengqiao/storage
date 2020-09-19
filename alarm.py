# -*- coding: utf-8 -*-

import time
import hashlib
import json
import urllib
import requests
import hmac
from random import seed 
from random import randint
from random import random 
import random
import datetime
import os
import copy
import operator
import logging, pdb
import base64

from enum import Enum, unique

# ------------------------------------------------------------------------
# CB uada
@unique
class StatusErrorCode(Enum):
    """docstring for StatusCode"""
    balance_insufficient = -2

class CoinBig():
    def __init__(self):
        self.base_url = 'https://www.coinbig.com/api/publics/vip'
        self.time = 3
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.timeout = 10

    def auth(self, key , secret):
        self.apiKey = key
        self.secret = secret

    def handler_error_if_needed(self, json):
        status = json['code']
        if status == StatusErrorCode.balance_insufficient.value:
            raise Exception(status)
        

    def sign(self, params):
        params["time"] = int(round(time.time() * 1000))
        _params = copy.copy(params)
        sort_params = sorted(_params.items(), key=operator.itemgetter(0))
        sort_params = dict(sort_params)
        sort_params['secret_key'] = self.secret
        string = urllib.parse.urlencode(sort_params)
        # _sign1 = hashlib.md5(bytes('abc'.encode('utf-8'))).hexdigest().upper()
        _sign = hashlib.md5(bytes(string.encode('utf-8'))).hexdigest().upper()
        params['sign'] = _sign
        return params

    def public_request(self, method, api_url, **payload):
        shouldRepeat = True
        while shouldRepeat:
            try:
                r_url = self.base_url + api_url
                if method == 'POST':
                    r = requests.request(method, r_url, json=payload, timeout = self.timeout, headers = self.headers)
                else:
                    r = requests.request(method, r_url, params=payload, timeout = self.timeout, headers = self.headers)
                logging.info(r)
            except Exception as err:
                logging.info('%s'%(err))
                time.sleep(self.time)
                
            else:
                r.raise_for_status()

                if r.status_code == 200 and r.json()['code'] == 0:
                    logging.info('%s'%(r.json()))
                    return r.json()
                else:
                    logging.info('%s'%(r.json()))
                    self.handler_error_if_needed(r.json())
                    time.sleep(self.time)
                    

    def signed_request(self, method, api_url, data = {}):
        new_data = copy.copy(data)
        new_data['apikey'] = self.apiKey
        # new_data['time'] = str(int(time.time() * 1000))
        print('new_data', new_data)
        try:
            url = self.base_url + api_url
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            r = requests.request('POST', url, data = self.sign(new_data), headers = headers)
            
        except Exception as err:
            logging.info('err %s'%(err))
            time.sleep(self.time)
            
        else:
            r.raise_for_status()
            if r.status_code == 200 and r.json()['code'] == 0:
                self.handler_error_if_needed(r.json())
                logging.info('success %s'%(r.json()))
                return r.json()
            else:
                logging.info('not 200 %s'%(r.json()))
                self.handler_error_if_needed(r.json())
                time.sleep(self.time)

    def tickers(self,symbol):
        return self.public_request('GET', '/trades',symbol=symbol)
    def depth(self, symbol):
        return self.public_request('GET', '/depth', symbol = symbol)


a=CoinBig()
# a.auth()
print(a.depth('btc_usdt')['data']['asks'][0][0])
print(a.tickers('uada_usdt'))


# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0' }
# r = requests.get('https://www.coinbig.com/api/publics/vip/tickers' , headers = headers)
# print(r.text)

# stop = False
# while stop == False:
#     rn = str(datetime.datetime.now().time())
#     print(rn)
#     if rn >= "22:01:10.000000":
#         stop = True
#         os.system("afplay 1.mp3")



HBO_URL = 'https://openapi.hboex.io'
Glen_URL = 'https://rest.glenbit.com/api'
# CB_URL = 'https://www.coinbig.com'

# def get_CB_trades(symbol_str):
#     params = dict()
#     params['symbol'] = symbol_str

#     url = CB_URL + '/api/publics/vip/trades'
#     response_data = http_get_request(url, params)
#     return response_data



# ------------------------------------------------------------------------
# get trades (HBO uada)

def get_trades(symbol_str):
    params = dict()
    params['symbol'] = symbol_str

    url = HBO_URL + '/open/api/get_trades'
    response_data = http_get_request(url, params)
    return response_data

def http_get_request(url, params):
    post_data = urllib.parse.urlencode(params)
    return http_request('GET',url,post_data)

# ------------------------------------------------------------------------
# get trades (GLB)

def get_glen_ticker(symbol_str):

    url = Glen_URL + "/v1/depth_n_history"
    data = {'pair': symbol_str}
    response_data = http_post2_request(url, data)
    return response_data

def http_post2_request(url, data):
    return http_request('POST',url, data=data, params=None)

def http_request(method_type, url, params, data=None, add_to_headers=None):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        "Accept": "application/json",
    }
    # if add_to_headers:
    #     headers.update(add_to_headers)
    while True:

        try:
            response = requests.request(method_type, url=url, params=params, data=data, headers=headers, timeout=45)
            if response.status_code == 200:
                return response.json()
            else:
                print(response.text)
                return
            break
        except KeyboardInterrupt:
            return
        except BaseException as e:

            print("%s , %s" % (url, e))
            # return
dt = get_trades('uada1234usdt')['data'][0]['ds']
print(dt)


dt = get_glen_ticker('GLB-USDT')['history'][0]
print(dt)

dt = get_glen_ticker('TANG-USDT')['history'][0]
print(dt)

dt = get_CB_trades('btc_usdt')
print(dt)

















