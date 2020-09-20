from baseclasses.strategy import BaseStrategy
from models import Order


class Strategy(BaseStrategy):
    """ Write your strategy here.

    data:
        self.symbol
        self.symbol_name
        self.price_data
    """

    def buy(self):
        if self.price_data['SMA_FAST'][-1] > self.price_data['SMA_SLOW'][-1]:
            print('BUY', self.symbol_name)
            Order(self.symbol_name).buy(
                self.price_data['close'][-1],
                self.price_data['timestamp'][-1]
            )

    def sell(self, buy_order):
        if self.price_data['SMA_FAST'][-1] < self.price_data['SMA_SLOW'][-1]:
            price_change = buy_order.price_change(self.price_data['close'][-1])
            print('SELL {0} at {1}%'.format(self.symbol_name, price_change))
            buy_order.sell(
                self.price_data['close'][-1],
                self.price_data['timestamp'][-1]
            )
