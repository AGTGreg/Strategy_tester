import gc_settings as _settings
from data_utils import data_manager
import backtester
from strategy import Strategy
from utils import plot


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
    test_strategy_against(['ADA_USDT', 'ZIL_USDT', 'BTC_USDT', 'ETH_USDT'])
