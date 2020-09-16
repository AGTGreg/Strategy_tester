import gc_globals as _globals
import gc_settings as _settings
from data_utils import data_manager
from testing_utils import backtester
from strategy import Strategy


def update_local_data():
    _settings.USE_LOCAL_DATA = False
    _settings.SAVE_DATA = True
    data_manager.init_data()


def test_strategy_against(markets):
    _settings.USE_LOCAL_DATA = True
    data_manager.init_data(markets)
    st = Strategy()
    backtester.test_strategy(st)


if __name__ == "__main__":
    # update_local_data()
    test_strategy_against(['ZIL_USDT'])
