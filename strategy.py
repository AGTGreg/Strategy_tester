from baseclasses.strategy import BaseStrategy
from trades_manager import place_new_order, ORDERS


class Strategy(BaseStrategy):

    def buy(self):
        if (
            self.price_data['MACD_H'][-1] > self.price_data['MACD_H'][-2] and
            max(self.price_data['MACD_H'][-3:]) < 0 and
            self.price_data['RSI'][-1] <= 35 and
            self.price_data['SMA_FAST'][-1] < self.price_data['SMA_SLOW'][-1]
        ):
            place_new_order('BUY', self.symbol_name)

        for trade in ORDERS:
            print(trade)

    def sell(self):
        if self.price_data['RSI'][-1] > 50:
            print('SELL!')
