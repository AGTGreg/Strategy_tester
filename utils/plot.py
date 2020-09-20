import numpy as np
import matplotlib.pyplot as plt
import gc_globals as _globals

from data_utils.indicators import compute_indicators


def plot_results(symbol_name):
    market = _globals.MARKETS[symbol_name]
    prices = market['price_history'].to_dict('series')

    indicators = compute_indicators(prices)

    fig, ax = plt.subplots()

    fig.set_size_inches(20, 10)

    ax.plot(
        prices['timestamp'],
        prices['close'],
        label="Price",
        c="navy"
    )

    ax.plot(
        prices['timestamp'],
        indicators['SMA_FAST'],
        label="SMA Fast",
        c="orange"
    )

    ax.plot(
        prices['timestamp'],
        indicators['SMA_MED'],
        label="SMA Medium",
        c="hotpink"
    )

    ax.plot(
        prices['timestamp'],
        indicators['SMA_SLOW'],
        label="SMA Slow",
        c="teal"
    )

    for order_id, order in _globals.BUY_ORDERS.items():
        if (order.symbol_name == symbol_name):
            ax.axvline(order.created, c='green')

    for order_id, order in _globals.SELL_ORDERS.items():
        if (order.symbol_name == symbol_name):
            ax.axvline(order.created, c='red')

    plt.xlabel('Time')
    plt.ylabel('Price')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)

    plt.show()
