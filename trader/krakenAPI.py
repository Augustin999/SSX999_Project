import base64
import hashlib
import hmac
import json
import time as tm
import urllib
import urllib.request as urllib2
from pandas.core import api

import requests as re

from trader import config, utils


def request(api_method, api_data):
    """
    Prepare, send and return a raw request.
    """
    api_domain = "https://api.kraken.com"
    
    if api_method in config.API_PRIVATE or api_method in config.API_TRADING or api_method in config.API_FUNDING:

        api_path = "/0/private/"
        api_uri = api_domain + api_path + api_method

        api_nonce = str(int(tm.time()*1000))
        api_data = urllib.parse.urlencode(api_data)

        try:
            api_key = utils.read_file(path=config.public_key)
            api_secret_encoded = utils.read_file(path=config.private_key)

        except:
            raise KeysConfigException()
        
        api_secret = base64.b64decode(api_secret_encoded)
        api_postdata = api_data + '&nonce=' + api_nonce
        api_postdata = api_postdata.encode('utf-8')
        api_sha256 = hashlib.sha256(api_nonce.encode('utf-8') + api_postdata).digest()

        api_hmacsha512 = hmac.new(
            api_secret,
            api_path.encode('utf-8') + api_method.encode('utf-8') + api_sha256,
            hashlib.sha512
        )

        api_request = urllib2.Request(api_uri, api_postdata)
        api_request.add_header('API-Key', api_key)
        api_request.add_header('API-Sign', base64.b64encode(api_hmacsha512.digest()))

        api_reply = urllib2.urlopen(api_request).read()
        api_reply = json.loads(api_reply)


    elif api_method in config.API_PUBLIC:
        
        api_path = "/0/public/"
        api_request = re.get(
            api_domain + api_path + api_method,
            params=api_data,
            headers={'User-Agent': 'Kraken REST API'}
        )

        api_reply = api_request.json()

    else:
        raise ApiMethodDontExistException()
    
    if api_reply['error'] != []:
        raise ApiErrorException(api_reply['error'])

    return api_reply


class ApiErrorException(Exception):
    ...


class ApiMethodDontExistException(Exception):
    ...


class KeysConfigException(Exception):
    def __init__(self):
        self.message = "API public key and API private (secret) key must be in text files called API_Public_Key and API_Private_Key"


def ticker(base):
    """
    Get ticker information.
    For more details about the Kraken API:
    https://www.kraken.com/features/api

    Inputs :
        pair : comma delimited list of asset pairs to get info on

    Results :
        a : ask array
            price,
            whole lot volume,
            lot volume
        
        b : bid array
            price,
            whole lot volume,
            lot volume

        c : last trade closed array
            price,
            lot volume
        
        v : volume array
            today,
            last 24 hours
        
        p : volume weighted average price array
            today,
            last 24 hours
        
        t : number of trades array
            today,
            last 24 hours
        
        l : low array
            today,
            last 24 hours
        
        h : high array
            today,
            last 24 hours
        
        o : today's opening price
    
    N.B. : Today's prices start at 00:00:00 UTC
    """

    try:
        api_method = 'Ticker'
        pair = utils.set_pair(base)
        api_data = {'pair': pair}
        api_reply = request(api_method, api_data)
        api_reply = api_reply['result'][pair]
        for each in list(api_reply.keys())[:-1]:
            api_reply[each] = list(map(float, api_reply[each]))
        api_reply['o'] = float(api_reply['o'])
        return api_reply
    except:
        return ticker(base)


def add_order(api_data):
    """
    Add standard order.
    For more details about the Kraken API:
    https://www.kraken.com/features/api

    Inputs :
        api_data: dict
            {
                'pair': utils.set_pair(base),
                'type': 'buy',
                'ordertype': 'limit',
                'price': price,
                'volume': nEur/price,
                'orderflags': flags (list)
            }
    """
    api_method = 'AddOrder'
    api_reply = request(api_method, api_data)
    return api_reply


def OHLC(base, since=0):
    """
    Get OHLC data.
    
    Inputs :
        pair : asset pair to get OHLC data for
        interval : time frame interval in minutes (optional) :
            1 (default),
            5,
            15,
            30,
            60,
            240,
            1440,
            10080,
            21600
        since : return committed OHLC data since given id (optional, exclusive)
        
    Results:
        array of array entries :
            time (opening the candle),
            open,
            high,
            low,
            close,
            vwap,
            volume,
            count
        last : id to be used as since when pulling for new, committed OHLC data
        
    N.B. : Maximum data length returned at once : 720 values
    """
    try:
        api_method = 'OHLC'
        pair = utils.set_pair(base)
        api_data = {
            'pair': pair,
            'interval': config.TIME_FRAMES[config.PERIOD],
            'since': since
        }
        api_reply = request(api_method, api_data)
        last = api_reply['result']['last']
        #  The last entry is not committed yet, hence ignore it
        api_reply = api_reply['result'][pair][:-1]
        return api_reply, last
    except:
        return OHLC(base, since)
