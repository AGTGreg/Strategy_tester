from copy import deepcopy
from datetime import datetime
from dataclasses import dataclass, field
from gc_globals import BUY_ORDERS, SELL_ORDERS
from data_utils.fields import Field
from data_utils.field_validators import is_order_side, is_order_state


@dataclass
class Order:
    symbol_name: str = Field(str)
    price: float = Field(float, default=0.0)
    side: str = Field(str, validators=[is_order_side], default='BUY')
    state: str = Field(str, validators=[is_order_state], default='COMMITTED')
    active: bool = Field(bool, default=True)
    created: datetime = field(default_factory=datetime.now)

    def buy(self, price):
        self.side = 'BUY'
        self.price = price
        BUY_ORDERS.append(self)

    def sell(self, price):
        if self.side == 'BUY':
            sell_order = deepcopy(self)
            sell_order.buy_order = self
            sell_order.side = 'SELL'
            sell_order.price = price
            sell_order.state = 'COMMITTED'
            SELL_ORDERS.append(sell_order)
            self.active = False

    def price_change(self, current_price):
        price_diff = current_price - self.price
        if price_diff == 0:
            return price_diff
        return round((price_diff / self.price) * 100, 2)

    def hold_duration(self):
        return (datetime.now() - self.created).total_seconds()
