
class Strategy(object):
    
    def __init__(self):
        super().__init__()
    
    def buy(self):
        """ Returns True if the strategy dictates we should buy.
        """
        pass

    def sell(self):
        """ Returns true if the strategy dictates we should sell.
        """
        pass
