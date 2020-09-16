""" This module is responsible for initializing the exchange and updating all
the data we need such as markets and their prices and indicators.
"""

import os
import copy

import ccxt
import pandas as pd
from runium.core import Runium

import gc_settings as _settings
import gc_globals as _globals
from data_utils import indicators
from utils.time_utils import MSTimestamp
from utils.gc_profiler import time_function


def init_data(markets=None):
    """ Initialize the EXCHANGE object, get the availble markets and all their
    data. We need to run this in order to use the EXCHANGE and MARKETS objects.
    If USE_LOCAL_DATA is True then the eschange is not initialized and the
    MARKETS gets popullated by the local data.
    """
    if _settings.USE_LOCAL_DATA is False:
        _globals.EXCHANGE = init_exchange()

    _globals.CANDLESTICKS_COUNT = \
        _settings.PRICE_HISTORY_TIMEFRAME / _settings.CANDLESTICK_TIMEFRAME_INT

    if markets is None:
        _globals.MARKETS = load_all_available_markets()
    else:
        _globals.MARKETS = load_markets(markets)

    if bool(_globals.MARKETS):
        get_price_history()
        clean_markets_list()
        print('==> Finished initialization of {0} markets.'.format(
            len(_globals.MARKETS)))
    else:
        print('==> There are no markets to initialize :(')

    return True


def init_exchange():
    exchange = getattr(ccxt, _settings.EXCHANGE_ID)({
        'enableRatelimit': True,
        'rateLimit': 1000
    })
    return exchange


def load_all_available_markets():
    """ Get all the active markets that trade against our BASE_CURRENCY and are
    not included in our BLACKLIST.
    """
    markets = {}

    if _settings.USE_LOCAL_DATA is False:
        # Get the markets dict from the API. Keep only the active ones.
        all_markets = _globals.EXCHANGE.load_markets(True)
        for market, market_data in all_markets.items():
            if all([
                market_data['quote'] == _settings.BASE_CURRENCY,
                market not in _settings.BLACKLIST,
                market_data['active'] is True
            ]):
                markets[market] = market_data

    else:
        # Create a markets dict from the files fount in MARKETS_DATA_PATH.
        mp = _settings.MARKETS_DATA_PATH
        markets_list = \
            [f for f in os.listdir(mp) if os.path.isfile(os.path.join(mp, f))]
        markets = {mrkt.replace('.csv', ''): {} for mrkt in markets_list}

    return markets


def load_markets(markets):
    """ Loads the data of the specified markets. Works only in LOCAL_DATA mode.
    """
    markets_data = {}
    for market in markets:
        market_path = \
            os.path.join(_settings.MARKETS_DATA_PATH, market + '.csv')
        if os.path.isfile(market_path):
            markets_data[market] = {}
    
    return markets_data


@time_function
def get_price_history():
    """ Initializes all the available markets with their price history.
    Performs some basic statistical analysis and applies indicators.
    """
    # Get a timestamp from the time declared in PRICE_HISTORY_TIMEFRAME
    # relative to now.
    # ie: If the timeframe is 10 mins, get the timestamp from 10 mins ago.
    ph_timeframe = _settings.PRICE_HISTORY_TIMEFRAME
    since = MSTimestamp().minus(ph_timeframe, 'm')

    rn = Runium(mode='multiprocessing')
    market_tasks = []

    for symbol_name in _globals.MARKETS.keys():
        task = rn.new_task(
            fetch_market_price_history,
            kwargs={
                'symbol_name': symbol_name,
                'since': since,
                'exchange': _globals.EXCHANGE
            }
        ).run()

        market_tasks.append(task)

    # Update the a market as soon as a task has finished.
    for task in market_tasks:
        data = task.result()
        _globals.MARKETS[data['symbol_name']].update(data)


def fetch_market_price_history(symbol_name, since, exchange):
    """ Returns the price_history (as a DataFrame) and state for the specified
    market. If anything goes wrong, or if there is not enough data, marks that
    market as inactive and returns no prices.
    """
    print('==> Fetching prices for', symbol_name)

    data = {'symbol_name': symbol_name, 'price_history': None, 'active': True}

    if _settings.USE_LOCAL_DATA is False:
        try:
            prices = exchange.fetch_ohlcv(
                symbol_name, _settings.CANDLESTICK_TIMEFRAME, since)
        except BaseException as err:
            print(err)
            data['active'] = False
            return data
        else:
            # The market does not have enough data. Mark it as not-active and
            # return.
            if len(prices) < _globals.CANDLESTICKS_COUNT:
                print('==> {0} does not have enough data.'.format(symbol_name))
                data['active'] = False
                return data

            data['price_history'] = pd.DataFrame.from_records(
                prices,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )

            if _settings.SAVE_DATA is True:
                csv_path = os.path.join(
                    _settings.MARKETS_DATA_PATH,
                    symbol_name.replace('/', '_') + '.csv'
                )
                data['price_history'].to_csv(
                    csv_path, index=True, header=True)

    else:
        # Load local data
        data['price_history'] = pd.read_csv(
            os.path.join(_settings.MARKETS_DATA_PATH, symbol_name + '.csv'),
            header=0, index_col=0
        )

    return data


def clean_markets_list():
    """ Iterates through the list of our available markets and removes the ones
    that are not active.
    """
    print('==> Cleaning markets list.')

    tmp_markets = copy.deepcopy(_globals.MARKETS)
    for m, m_data in _globals.MARKETS.items():
        if m_data['active'] is False:
            del tmp_markets[m]

    _globals.MARKETS = copy.deepcopy(tmp_markets)


def analyse_market(data):
    """ Performs a basic statistics analysis of the price history and adds
    indicators to the data.
    """
    symbol_name = data['symbol_name']

    try:
        print('==> Analysing {0}'.format(symbol_name))
        inds = indicators.compute_indicators(data['price_history'])
    except BaseException as err:
        print(err)
        data['active'] = False
    else:
        data['indicators'] = inds

    return data
