import gc_globals as _globals
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

    def run(self, symbol_name, price_history):
        self.symbol_name = symbol_name
        indicators = compute_indicators(price_history)
        price_history.update(indicators)
        self.price_data = price_history

        self.buy()
        for order in _globals.BUY_ORDERS:
            if order.active is True and order.symbol_name == self.symbol_name:
                self.sell(order)

    def buy(self):
        """ Returns True if the strategy dictates we should buy.
        """
        pass

    def sell(self, buy_order):
        """ Returns true if the strategy dictates we should sell.
        """
        pass
