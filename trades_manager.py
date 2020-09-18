from types import SimpleNamespace

ORDERS = []


def place_new_order(side, symbol_name, price):
    if side not in ORDER_SIDES:
        raise BaseException('Side must be one of {0}'.format(ORDER_SIDES))

    new_order = SimpleNamespace(
        side=side,
        state='NEW',
        symbol_name=symbol_name,
        price=price
    )

    ORDERS.append(new_order)

    return new_order
