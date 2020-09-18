ORDER_STATES = ['NEW', 'CLOSED', 'CANCELED', 'COMMITTED']
ORDER_SIDES = ['BUY', 'SELL']


def is_order_state(name, value):
    if value not in ORDER_STATES:
        raise ValueError("{0} must be one of {1}".format(name, ORDER_STATES))


def is_order_side(name, value):
    if value not in ORDER_SIDES:
        raise ValueError("{0} must be one of {1}".format(name, ORDER_SIDES))
