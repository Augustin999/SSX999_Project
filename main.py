# SSX999 Project
#
# Augustin BRISSART
# Github: @augustin999
#
#
# main.py

import config
from trader import init_trading_bot, update_trading_bot

if __name__ == '__main__':

    # Case : initializing the algorithm
    if not config.wallet_path.exists():
        init_trading_bot()

    # Case : algorithm already initialized
    else:
        update_trading_bot()
