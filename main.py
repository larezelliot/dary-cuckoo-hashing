"""CSE6041"""

import random
from statistics import mean, median, stdev

import matplotlib.pyplot as plt
from hashTable import RandomWalkHashTable
from tqdm import tqdm

from utils import get_random_key


# TODO: Share seed across modules
# random.seed(1)


def main():
    d = 2

    for size in [1_000, 10_000, 100_000]:
        for load_factor in [0.85]:
            table = RandomWalkHashTable(size, load_factor, d=3, max_displacements=d*size)
            random_keys = [get_random_key() for i in range(10_000)]

            failed_insertion = 0
            displacements_arr = []

            for key in random_keys:
                was_inserted, displacements = table.insert_key(key, dry_run=True)

                if not was_inserted:
                    failed_insertion += 1
                    continue

                displacements_arr.append(displacements)

            print(f"{size=} {load_factor=}")
            # print(f"\tFailed: {failed_insertion=}")
            # print(f"\tMIN: {min(displacements_arr)}")
            # print(f"\tMAX: {max(displacements_arr)}")
            print(f"\tMean: {mean(displacements_arr):2f}")
            # print(f"\tMedian: {mean(displacements_arr):2f}")
            print(f"\tSTD: {stdev(displacements_arr):2f}")

        print()


if __name__ == "__main__":
    main()
