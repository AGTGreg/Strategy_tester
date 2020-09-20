import numpy as np

import gc_globals as _globals
import gc_settings as _settings
from utils.plot import plot_results
from utils.gc_profiler import time_function


@time_function
def test_strategy(strategy):
    """ Test a strategy against all loaded markets.
    """
    for symbol_name, market in _globals.MARKETS.items():
        print(symbol_name)
        walk_prices(market, strategy)
        # plot_results(symbol_name)


def walk_prices(market, strategy):
    """ Iterates over the prices and indicator data and tests the strategy
    against them.
    """
    print('==> Testing strategy against {0}'.format(market['symbol_name']))

    prices = \
        market['price_history'].head(
            _settings.TESTING_TIMEFRAME).to_dict('series')

    for index, row in market['price_history'].iterrows():
        # Allways keep TESTING_TIMEFRAME amount of candlesticks.
        if index >= _settings.TESTING_TIMEFRAME:
            for index, value in row.items():
                prices[index] = np.append(prices[index], value)[1:]
            strategy.run(market, prices)
