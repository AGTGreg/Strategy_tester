import pandas as pd
import numpy as np
from data_utils.indicators import compute_indicators


class BaseStrategy(object):
    """ The strategy is where all the decision making takes place.
    First, the check_prices method is called, self.prices gets populated with a
    DataFrame with ohlcv data.
    Then the strategy should perform any action is nessessary that will help in
    making a decision. Usually that means to apply indicators.

    Every strategy should inherit from this.
    """
    def __init__(self):
        self.symbol_name = None
        self.price_data = None

    def check_prices(self, symbol_name, price_history):
        self.symbol_name = symbol_name
        indicators = compute_indicators(price_history)
        price_history.update(indicators)
        self.price_data = price_history

        self.buy()
        self.sell()

    def buy(self):
        """ Returns True if the strategy dictates we should buy.
        """
        pass

    def sell(self):
        """ Returns true if the strategy dictates we should sell.
        """
        pass
