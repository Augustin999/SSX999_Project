# SSX999 Project
#
# Augustin BRISSART
# Github: @augustin999


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
    logger.info('Continuing trading')

    #  load existing wallet
    wallet = utils.load_pickle(path=config.wallet_path)
    
    #  load previous OHLC data from csv file
    universe_lasts = utils.load_pickle(path=config.lasts_path)

    for base in wallet.universe:

        data = dataManager.load_OHLC_data(base)
        #  update OHLC data
        previous_last = universe_lasts[base]
        data, last = dataManager.update_OHLC_data(base, data, previous_last)

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
            'HA_close_current': data['HA_close'].values[-1],
            'HA_open_current': data['HA_open'].values[-1],
            'ema_current': data['ema'].values[-1],
            'bollinger_center_previous': data['bollinger_center'].values[-2],
            'bollinger_center_current': data['bollinger_center'].values[-1],
            'cci_previous': data['cci'].values[-2],
            'cci_current': data['cci'].values[-1],
            'last_position': position
        }
        
        # compute strategy
        new_position = analyzer.strategy_CCI(features)
        
        # execute orders
        wallet.currencies[base].update_price()
        
        if new_position == 1:
            wallet.currencies[base].buy()
            logger.info(f'Buy {base}')
            #  If previous position was 1 too, buy() will automatically not create a new order
            
        elif new_position == 0:
            wallet.currencies[base].sell()
            logger.info(f'Sell {base}')
            #  If previous position was 0 too, buy() will automatically not create a new order

    # persist the wallet's new composition and the lasts values
    utils.dump_as_pickle(content=wallet, path=config.wallet_path)
    utils.dump_as_pickle(content=universe_lasts, path=config.lasts_path)
    
    # store performances
    wallet.update_performances()

    #  Inform of the bot's process complleted normally
    logger.info('Strategy performed successfully')
