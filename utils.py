"""utils.py"""

from functools import partial
import random


import mmh3


def get_random_key(n=8) -> bytes:
    """Returns a random key with of length n"""

    return random.randbytes(n)


def get_hashing_functions(d):
    """Returns a list of d random hashing functions"""

    # TODO: seed
    return [partial(mmh3.hash, seed=i) for i in range(d)]
