import time


class MSTimestamp(object):
    """ Returns and manimulates a timestamp in ms. Default is the current
    timestamp.
    """

    def __init__(self, current=None):
        if current is None:
            self.current = int(round(time.time()) * 1000)
        else:
            self.current = (current * 1000)

    def get_timestamp(self):
        return self.current

    def minus(self, value, scale='ms'):
        if scale == 's':
            return self.current - (value * 1000)
        elif scale == 'm':
            return self.current - (value * 60000)
        elif scale == 'h':
            return self.current - (value * 3600000)
        else:
            return self.current - value

    def plus(self, value, scale='ms'):
        if scale == 's':
            return self.current + (value * 1000)
        elif scale == 'm':
            return self.current + (value * 60000)
        elif scale == 'h':
            return self.current + (value * 3600000)
        else:
            return self.current + value

    def verbose(self, to_datetime=True):
        if to_datetime is True:
            return time.strftime('%d-%m-%Y %H:%M:%S', self.current / 1000)
        else:
            return time.strftime('%H:%M:%S', self.current / 1000)

    
