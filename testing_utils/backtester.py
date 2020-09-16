import pandas as pd
import numpy as np
from runium.core import Runium

import gc_globals as _globals
import gc_settings as _settings


def test_strategy(strategy):
    """ Test a strategy against all markets.
    """
    rn = Runium(mode='multiprocessing')
    trade_tasks = []

    print('='*100)

    # For debuging
    symbol_name = list(_globals.MARKETS.keys())[0]
    walk_prices(symbol_name, strategy)

    # For production
    # for symbol_name in _globals.MARKETS:
    #     task = rn.new_task(
    #         walk_prices,
    #         kwargs={'symbol_name': symbol_name, 'strategy': strategy}
    #     ).run()


def walk_prices(symbol_name, strategy):
    """ Iterates over the prices and indicator data and tests the strategy
    against them.
    """
    print('==> Testing strategy against {0}'.format(symbol_name))

    market = _globals.MARKETS[symbol_name]

    print('==> Prices: {0}, RSI: {1}, SMA_FAST: {2}, SMA_MED: {3}, SMA_SLOW: {4}, MACD_H: {5}'.format(
        len(market['price_history']), len(market['indicators']['RSI']),
        len(market['indicators']['SMA_FAST']),
        len(market['indicators']['SMA_MED']),
        len(market['indicators']['SMA_SLOW']),
        len(market['indicators']['MACD_H'])
    ))
    
    inds = market['indicators']
    for index, row in market['price_history'].iterrows():
        print('='*50)
        print(index)
        print(row.close)
        print(inds['SMA_FAST'].iloc[index])
