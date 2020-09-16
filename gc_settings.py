""" The entire program can be controlled within this file.
"""
import os

# The id of the exchange we want to use
EXCHANGE_ID = 'binance'

# The symbol we want to trade against. All the available markets will be
# filtered against this value so the markets available to us will be the ones
# that use this base currency.
BASE_CURRENCY = 'USDT'

# The markets of those symbols will be removed from the markets list.
BLACKLIST = ['BNB/USDT', 'TUSD/USDT', 'USDC/USDT', 'USDS/USDT', 'PAX/USDT']

# The candlesticks timeframe possible values are 1m, 5m, 15m, 1h, 1d
CANDLESTICK_TIMEFRAME = '5m'

# The candlesticks timeframe as integer in minutes
CANDLESTICK_TIMEFRAME_INT = 5

# The number of minutes of price history to keep for each market.
PRICE_HISTORY_TIMEFRAME = 1440  # 1 day

# If the path where our data is.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOCAL_DATA_PATH = os.path.join(BASE_DIR, 'data')
MARKETS_DATA_PATH = os.path.join(LOCAL_DATA_PATH, 'markets')

# Set this to True if you want to use the local data instead of fetching it
# from the API
USE_LOCAL_DATA = False

# Set this to True if you want to save the prices data fetched from the API to
# csv files. (USE_LOCAL_DATA must be False)
SAVE_DATA = True
