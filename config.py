from pathlib import Path


data_dir = Path('historical_data')
generated_data_dir = Path('generated_data')

wallet_path = generated_data_dir / 'wallet.pickle'
performances_path = generated_data_dir / 'performances.csv'
lasts_path = generated_data_dir / 'lasts.pickle'
log_path = generated_data_dir / 'logs.txt'

QUOTE = 'EUR'
PERIOD = '4h'
CAPITAL = 100
UNIVERSE = ['XBT', 'ETH', 'XMR', 'QTUM', 'ADA', 'MLN', 'ZEC']
DATA_COLUMNS = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
FEE_RATE = 0.16 / 100
CSV_SEP = ','

TIME_FRAMES = {
    '1mn': 1,
    '5mn': 5,
    '15mn': 15,
    '30mn': 30,
    '1h': 60,
    '4h': 240,
    '1d': 1440,
    '1w': 10080,
    '15d': 21600
}

BASES = [
    'ETC', 'XMR', 'QTUM', 'ATOM',
    'XLM', 'DAI', 'XRP', 'LINK',
    'PAXG', 'GNO', 'REP', 'XDG',
    'MLN', 'ETH', 'ADA', 'BAT',
    'LSK', 'TRX', 'DASH', 'XTZ',
    'NANO', 'XBT', 'LTC', 'SC',
    'WAVES', 'ALGO', 'EOS', 'OMG',
    'BCH', 'ICX', 'ZEC'
]

SPECIAL_BASES = [
    'QTUM', 'ATOM', 'LINK', 'PAXG',
    'GNO', 'XDG', 'ADA', 'BAT',
    'LSK', 'TRX', 'DASH', 'XTZ',
    'NANO', 'WAVES', 'SC', 'ALGO',
    'EOS', 'OMG', 'BCH', 'ICX', 'DAI'
]

API_PUBLIC = {
    'Time',
    'Assets',
    'AssetPairs',
    'Ticker',
    'OHLC',
    'Depth',
    'Trades',
    'Spread'
}

API_PRIVATE = {
    'Balance',
    'TradeBalance',
    'OpenOrders',
    'ClosedOrders',
    'QueryOrders',
    'TradesHistory',
    'QueryTrades',
    'OpenPositions',
    'Ledgers',
    'QueryLedgers',
    'RemoveExport',
    'GetWebSocketsToken'
}

API_TRADING = {'AddOrder', 'CancelOrder'}

API_FUNDING = {
    'DepositMethods',
    'DepositAddresses',
    'DepositStatus',
    'WithdrawInfo',
    'Withdraw',
    'WithdrawStatus',
    'WithdrawCancel',
    'WalletTransfer'
}
