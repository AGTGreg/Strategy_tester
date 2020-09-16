import gc_globals as _globals
from data_utils import data_manager
from testing_utils import backtester
from strategy import Strategy


def start():
    if _globals.ACTIVE is False:
        data_manager.init_data()
        
        st = Strategy()
        backtester.test_strategy(st)
        
        _globals.ACTIVE = True


if __name__ == "__main__":
    start()
