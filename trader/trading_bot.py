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

import logging
import pickle

from trader import analyzer, config, dataManager, utils
from trader.models import Wallet

logger = logging.getLogger('trader')
logger.setLevel(logging.DEBUG)


def init_trading_bot():
    logger.info('Initializing a new trading bot')

    if not config.generated_data_dir.exists():
        config.generated_data_dir.mkdir()
    if not config.data_dir.exists():
        config.data_dir.mkdir()

    #  Create a new wallet and save it
    structure = {
        'initialize': True,
        'capital': config.CAPITAL,
        'universe': config.UNIVERSE
    }
    wallet = Wallet(structure)
    wallet.create_performances()
    utils.dump_as_pickle(content=wallet, path=config.wallet_path)

    # pull data from api
    universe_lasts = dict()
    for base in wallet.universe:
        last = dataManager.pull_OHLC_data(base)
        universe_lasts[base] = last

    # store lasts
    utils.dump_as_pickle(content=universe_lasts, path=config.lasts_path)

    #  inform of successful initialization
    logger.info('Initialisation: completed')


def update_trading_bot():
    #  first, check if time is right according to timescale
    logger.info('Checking time exactitude')

    #  load existing wallet
    wallet = utils.load_pickle(path=config.wallet_path)
    
    for base in wallet.universe:
        #  load previous OHLC data from csv file
        data = dataManager.load_OHLC_data(base)
        universe_lasts = utils.load_pickle(path=config.lasts_path)

        #  update OHLC data
        previous_last = universe_lasts[base]
        logger.info(utils.toTs(previous_last))
        data, last = dataManager.update_OHLC_data(base, data, previous_last)
        logger.info(utils.toTs(last))

        #  if last did not change, abort and wait for new candle
        if previous_last >= last:
            logger.error('Time not corresponding')
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
    utils.dump_as_pickle(content=wallet, path=config.wallet_path)
    utils.dump_as_pickle(content=universe_lasts, path=config.lasts_path)

    # store performances
    wallet.update_performances()

    #  Inform of the bot's process complleted normally
    logger.info('Strategy performed successfully')
