"""utils.py"""

from functools import partial
import math
import random

import mmh3


def get_random_key(n=8) -> bytes:
    """Returns a random key with of length n."""

    return random.randbytes(n)


def get_hashing_functions(d: int):
    """Returns a list of d random hashing functions."""

    # TODO: seed
    return [partial(mmh3.hash, seed=i) for i in range(d)]


def get_optimal_max_displacements(n: int, m: int) -> int:
    """Returns the value of MaxLoop."""

    # TODO: This is the formula for max displacement
    # presented in the original cuckoo paper

    n = max(n, 100)
    max_displacements = math.ceil(3 * math.log(n, m))
    return max_displacements
