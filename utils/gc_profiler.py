import time


def time_function(f):
    """ Times any function and prints the result. Use it as a decorator.
    """
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(
            '==> Function [',
            f.__name__,
            '] finished in',
            '{0:.3f}'.format(end - start),
            'seconds.'
        )
        return result
    return f_timer
