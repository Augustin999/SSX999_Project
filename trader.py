# SSX999 Project
#
# Augustin BRISSART
# Github: @augustin999
#
#
# trader.py
#
#       Compute strategy and execute orders
#
        # load latest wallet              || create a new wallet
        # load previous OHLC data         || pull data from api
        # update OHLC data                || stop here & wait for the next order opportunity
        # compute indicators on data
        # prepare data features required for strategy
        # compute strategy
        # execute orders
        # update wallet composition
        # store performances & wallet composition
        # erase any unecessary variable left

import numpy as np
import pandas as pd
import pickle
import os

from classes import Wallet, Currency
import utils
import dataManager
import analyzer

if __name__ == '__main__':

    # Case : initializing the algorithm
    if not os.path.exists(utils.WALLET_PATH):

        print('Initializing a new trading bot')

        #  Create a new wallet and save it
        structure = {
            'initialize': True,
            'capital': utils.CAPITAL,
            'universe': utils.UNIVERSE
        }
        wallet = Wallet(structure)
        wallet.create_performances()
        dataManager.save_wallet(wallet)

        # pull data from api
        universe_lasts = dict()
        for base in wallet.universe:
            last = dataManager.pull_OHLC_data(base)
            universe_lasts[base] = last

        # store lasts
        with open(utils.LASTS_PATH, 'wb') as f_lasts:
            pickle.dump(universe_lasts, f_lasts)
        
        #  delete any unecessary variable left to preserve memory
        del(structure)
        del(wallet)
        del(last)
        del(universe_lasts)

        #  inform of successful initialization
        print('Initialisation: completed')
    

    # Case : algorithm already initialized
    else:
        #  first, check if time is right according to timescale
        print('Checking time exactitude')

        #  load existing wallet
        wallet = dataManager.load_wallet() 
        
        for base in wallet.universe:
            #  load previous OHLC data from csv file
            data = dataManager.load_OHLC_data(base)
            universe_lasts = pickle.load(open(utils.LASTS_PATH, 'rb'))

            #  update OHLC data
            previous_last = universe_lasts[base]
            print(utils.toTs(last))
            data, last = dataManager.update_OHLC_data(base, data, previous_last)

            #  if last did not change, abort and wait for new candle
            if previous_last >= last:
                utils.log_error('Time not corresponding')
                break

            universe_lasts[base] = last
            dataManager.update_OHLC_data_csv(base, data)
            
            # compute indicators on data
            data = analyzer.compute_indicators(data)

            # prepare data features required for strategy
            if wallet.currencies[base].buyable():
                position = 0
            else:
                position = 1

            features = {
                    'HA_open': data['HA_open'].values[-1],
                    'HA_close': data['HA_close'].values[-1],
                    'mfi_prev': data['mfi'].values[-2],
                    'mfi_curr': data['mfi'].values[-1],
                    'lastPosition': position
                }
            
            # compute strategy
            new_position = analyzer.strategy_HA_MFI(features)

            # execute orders
            if new_position == 1:
                wallet.currencies[base].buy()
                #  If previous position was 1 too, buy() will automatically not create a new order
            elif new_position == 0:
                wallet.currencies[base].sell()
                #  If previous position was 0 too, buy() will automatically not create a new order

        # persist the wallet's new composition and the lasts values
        dataManager.save_wallet(wallet)
        with open(utils.LASTS_PATH, 'wb') as f_lasts:
            pickle.dump(universe_lasts, f_lasts)

        # store performances
        wallet.update_performances()
        
        #  delete any unecessary variable left to preserve memory
        del(wallet)
        del(features)
        del(data)
        del(position)
        del(new_position)
        del(universe_lasts)
        del(last)

        #  Inform of the bot's process complleted normally
        print('Strategy performed successfully')

















    

