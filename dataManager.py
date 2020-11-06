import pickle

import pandas as pd

import config
import krakenAPI
import utils


def buy(base, nEur, post=True):
    """
    Execute a buy order with the following specs :
        type : limit order
        fees : applied in quote currency
        quote : eur
    By default, post is set to True to garantee maker fees are applied.

    Inputs:
        base: base to buy (uppercase)
        nEur: amount of euros to spend
        post: boolean
    """

    flags = ['fciq', 'post']
    if not post:
        flags = ['fciq']

    ticker = krakenAPI.ticker(base)
    bid = ticker['b'][0]
    price = round(bid, 2)

    api_data = {
        'pair': utils.set_pair(base),
        'type': 'buy',
        'ordertype': 'limit',
        'price': price,
        'volume': nEur/price,
        'orderflags': flags
    }

    krakenAPI.add_order(api_data)

    return price

def sell(base, nBase, post=True):
    """
    Execute a buy order with the following specs :
        type : limit order
        fees : applied in quote currency
        quote : eur
    By default, post is set to True to garantee maker fees are applied.

    Inputs:
        base: base to buy (uppercase)
        nBase: amount of euros to spend
        post: boolean
    """

    flags = ['fciq', 'post']
    if not post:
        flags = ['fciq']

    ticker = krakenAPI.ticker(base)
    ask = ticker['a'][0]
    price = round(ask, 2)
    
    api_data = {
        'pair': utils.set_pair(base),
        'type': 'sell',
        'ordertype': 'limit',
        'price': price,
        'volume': nBase/price,
        'orderflags': flags
    }
    krakenAPI.add_order(api_data)
    return price

def get_price(base):
    """
    Returns the average between bid and ask, as a price.
    """
    ticker = krakenAPI.ticker(base)
    ask, bid = float(ticker['a'][0]), float(ticker['b'][0])
    price = (ask + bid) / 2
    return price

def save_wallet(wallet):
    """
    Persist the wallet.
    """
    pickle.dump(wallet, open(config.wallet_path,"wb"))
    return

def load_wallet():
    """
    Load an existing wallet.
    """
    return pickle.load(open(config.wallet_path, "rb"))

def pull_OHLC_data(base):
    # get data from api
    data, last = krakenAPI.OHLC(base)
    df_data = pd.DataFrame(data, columns=config.DATA_COLUMNS)
    df_data = df_data.astype(float)
    df_data.set_index('time', inplace=True)

    # store data into csv file
    pair = utils.set_pair(base)
    filename = pair + config.PERIOD + '.csv'
    path = config.data_dir / filename
    df_data.to_csv(path, sep=config.CSV_SEP, encoding='utf-8')

    return last

def load_OHLC_data(base):
    """
    Load previous data corresponding to base and that is stored in csv files.
    """
    pair = utils.set_pair(base)
    filename = pair + config.PERIOD + '.csv'
    path = config.data_dir / filename
    data = pd.read_csv(path, sep=config.CSV_SEP)
    data.set_index('time', inplace=True)
    return data

def update_OHLC_data(base, data, last):
    """
    Pull missing new data for base.
    Returns the updated, sorted dataframe.
    """
    #  Pull new, committed data corresponding to base 
    new_data, new_last = krakenAPI.OHLC(base, last)
    
    #  Shape the new dataframe like the previous one
    new_data = pd.DataFrame(new_data, columns=config.DATA_COLUMNS)
    new_data = new_data.astype(float)
    new_data.set_index('time', inplace=True)

    #  Merge previous and fresh data into a single dataframe
    data = data.append(new_data)
    data.sort_index(inplace=True)
    
    return data, new_last

def update_OHLC_data_csv(base, data):
    pair = utils.set_pair(base)
    filename = pair + config.PERIOD + '.csv'
    path = config.data_dir / filename
    data.to_csv(path, sep=config.CSV_SEP, encoding='utf-8')
    return
