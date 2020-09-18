import gc_globals as _globals
from models import Order


def new_buy_order(symbol_name, price):
    new_order = Order('BUY', symbol_name, price)
    _globals.BUY_ORDERS.append(new_order)
    return new_order
