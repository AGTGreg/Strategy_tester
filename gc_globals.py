""" Objects and variables that are used regullarly in multiple modules are
stored here as globals for convinience. This is NOT a settings module. The data
in the globals are just to initialize them. Do not change it. If you need to
change a setting go to gc_settings.py.
"""

ACTIVE = False
EXCHANGE = None
MARKETS = {}
ORDERS = []
BUY_ORDERS = []
SELL_ORDERS = []
BALANCE = 0

# This is the number of candlestics that every market's price_history should
# have in order to be considered worthy for saving.
# This value is the result of this:
# PRICE_HISTORY_TIMEFRAME / CANDLESTICK_TIMEFRAME
CANDLESTICKS_COUNT = 0
