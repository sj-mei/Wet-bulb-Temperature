import numpy as np

try:
    from numba import vectorize as _numba_vectorize
except Exception:
    _numba_vectorize = None


def vectorize(*args, **kwargs):
    if _numba_vectorize is not None:
        return _numba_vectorize(*args, **kwargs)

    def decorator(func):
        return np.vectorize(func)

    return decorator

