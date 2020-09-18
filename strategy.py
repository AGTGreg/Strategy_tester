from baseclasses.strategy import BaseStrategy
from models import Order


class Strategy(BaseStrategy):
    """ Write your strategy here. Don't use this one you'll lose your money if
    you do.
    """

    def buy(self):
        if self.price_data['RSI'][-1] <= 35:
            print('BUY!')
            Order(self.symbol_name).buy(self.price_data['close'][-1])

    def sell(self, buy_order):
        price_change = buy_order.price_change(self.price_data['close'][-1])
        if any([
            price_change > 2,
            price_change < -1
        ]):
            print('SELL at {0}%'.format(price_change))
            print('Holded for', buy_order.hold_duration())
            buy_order.sell(self.price_data['close'][-1])
