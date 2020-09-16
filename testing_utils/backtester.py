import pandas as pd
import numpy as np
from runium.core import Runium

import gc_globals as _globals
import gc_settings as _settings
from data_utils.indicators import compute_indicators


def test_strategy(strategy):
    """ Test a strategy against all loaded markets.
    """
    rn = Runium(mode='multiprocessing')
    trade_tasks = []

    for symbol_name in _globals.MARKETS:
        task = rn.new_task(
            walk_prices,
            kwargs={'symbol_name': symbol_name, 'strategy': strategy}
        ).run()
        trade_tasks.append(task)


def walk_prices(symbol_name, strategy):
    """ Iterates over the prices and indicator data and tests the strategy
    against them.
    """
    print('==> Testing strategy against {0}'.format(symbol_name))

    market = _globals.MARKETS[symbol_name]

    prices = market['price_history'].head(_settings.TESTING_TIMEFRAME).copy()

    for index, row in market['price_history'].iterrows():
        if index >= _settings.TESTING_TIMEFRAME:
            # Allways keep TESTING_TIMEFRAME amount of candlesticks.
            prices = prices.append(row)
            prices = prices[1:]

    print(prices.head(50))
