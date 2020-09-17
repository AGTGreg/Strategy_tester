from types import SimpleNamespace

import gc_globals as _globals


ORDERS = []

ORDER_STATES = ['NEW', 'CLOSED', 'CANCELED', 'COMMITED']
ORDER_SIDES = ['BUY', 'SELL']


def place_new_order(side, symbol_name, price=None):
    if side not in ORDER_SIDES:
        raise BaseException('Side must be one of {0}'.format(ORDER_SIDES))

    if price is None:
        price = _globals.MARKETS[symbol_name]['price_history']['close'][0]

    new_order = SimpleNamespace(
        side=side,
        state='NEW',
        symbol_name=symbol_name,
        price=price
    )

    ORDERS.append(new_order)

    return new_order
