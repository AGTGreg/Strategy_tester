import numpy as np
import pandas as pd


def compute_sma(prices, period):
    smaFrame = pd.DataFrame(prices)
    sma = smaFrame.rolling(window=period).mean()
    return sma


def compute_ema(prices, period):
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    a = np.convolve(prices, weights, mode='full')[:len(prices)]
    a[:period] = a[period]
    return a


def compute_rsi(prices, n=14):
    """ Computes the RSI of the given prices array. NaN values are converted to
    zeros. Returns a python readable list of integers in the range of 0-100.
    """
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = np.divide(up, down, out=np.zeros_like(up), where=down != 0)
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + np.nan_to_num(rs))

    for i in range(n, len(prices)):
        delta = deltas[i-1]

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = np.divide(up, down, out=np.zeros_like(up), where=down != 0)
        rsi[i] = 100. - 100. / (1. + np.nan_to_num(rs))

    return rsi


def compute_macd_histogram(prices, slow=26, fast=12, signal_frame=9):
    """ Compute the MACD (Moving Average Convergence/Divergence) using a fast
    and slow exponential moving average.
    Return value is macd histogram as a python readable list. If the price
    samples is less than slow (26) it returns a list of zeros.
    """
    if len(prices) < slow:
        return [0] * len(prices)
    ema_slow = compute_ema(prices, slow)
    ema_fast = compute_ema(prices, fast)
    macd = ema_fast - ema_slow
    signal = compute_ema(macd, signal_frame)
    macd_histogram = macd - signal
    return macd_histogram


def compute_indicators(price_history):
    """ Returns all the needed indicators in a pandas DataFrame.
    """
    close_prices = price_history['close'].values
    return {
        'SMA_FAST': compute_sma(close_prices, 3),
        'SMA_MED': compute_sma(close_prices, 6),
        'SMA_SLOW': compute_sma(close_prices, 20),
        'RSI': compute_rsi(close_prices, 14),
        'MACD_H': compute_macd_histogram(close_prices),
        'HIGHEST_HIGH': price_history['high'].max(),
        'LOWEST_LOW': price_history['low'].min()
    }
