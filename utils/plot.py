import numpy as np
import matplotlib.pyplot as plt
import gc_globals as _globals

from data_utils.indicators import compute_indicators


def plot_results(symbol_name):
    market = _globals.MARKETS[symbol_name]
    prices = market['price_history'].to_dict('series')

    indicators = compute_indicators(prices)

    fig, ax = plt.subplots()
    ax.plot(
        prices['timestamp'],
        prices['close'],

        prices['timestamp'],
        indicators['SMA_FAST'],

        prices['timestamp'],
        indicators['SMA_MED'],

        prices['timestamp'],
        indicators['SMA_SLOW']
    )

    plt.xlabel('Time')
    plt.ylabel('Price')

    plt.show()
