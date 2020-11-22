# SSX999 Project
#
# Augustin BRISSART
# Github: @augustin999
#
#
# main.py

from trader import config
from trader.trading_bot import init_trading_bot, update_trading_bot

def main(data, context):
    # `data` and `context` are not used in this project, but are required
    # for the code to be compatible with Cloud Function

    # Case : initializing the algorithm
    if not config.wallet_path.exists():
        init_trading_bot()

    # Case : algorithm already initialized
    else:
        update_trading_bot()


if __name__ == '__main__':
    main()
