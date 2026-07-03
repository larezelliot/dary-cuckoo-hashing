"""CSE6041"""

import random
from functools import partial
from typing import Optional

import matplotlib.pyplot as plt
import mmh3


random.seed(1)

MAX_DISPLACEMENTS  = 1000
NUM_KEYS = 1000
TABLE_SIZE = 500
NUM_HASH_FUNCTIONS = 10

T: list[Optional[bytes]] = [None] * TABLE_SIZE
hashing_functions = [partial(mmh3.hash, seed=i) for i in range(NUM_HASH_FUNCTIONS)]


def insert(key: bytes, t) -> tuple[bool, int] :
    """"""

    for i in range(MAX_DISPLACEMENTS):
        # Get candidate positions
        candidate_positions = [h_i(key) % TABLE_SIZE
                               for h_i in hashing_functions]

        # Try every candidate position
        for p in candidate_positions:
            if t[p] is None:
                t[p] = key
                return True, i

        # Randomly evict one resident
        pos = random.choice(candidate_positions)
        t[pos], key = key, t[pos]  # type: ignore

    return False, MAX_DISPLACEMENTS


def main():
    """"""
    success_arr = []
    displacement_arr = []

    for _ in range(NUM_KEYS):
        success, displacements = insert(random.randbytes(8), T)

        if success:
            displacement_arr.append(displacements)
        # print(f"{success=}\t{displacements=}")

    plt.plot(displacement_arr)
    plt.show()


if __name__ == "__main__":
    main()
