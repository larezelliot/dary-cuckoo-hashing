"""CSE6041"""

from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt
from config import D_VALUES, LOAD_FACTORS, N, OUTPUT_DIR, TABLE_SIZES
from hashTable import MaxDisplacementsExceededError, RandomWalkDaryHashTable

from utils import get_random_key


def simulate(d: int, table_size: int, load_factor: float):
    max_displacements = table_size * 2

    table = RandomWalkDaryHashTable(table_size, d, max_displacements, partitioned=False)

    try:
        table.fill_random(load_factor)
    except MaxDisplacementsExceededError:
        print(f"Unable to create {table} with load factor {load_factor}")
        return []  #HACK

    original_table = table.table.copy()

    # Create random keys and insert in the table, counting the number of displacements
    random_keys = [get_random_key() for _ in range(N)]
    displacement_arr = []

    for key in random_keys:
        # Revert the hash table to original value
        table.table = original_table.copy()

        # Attempt to insert into the table
        try:
            displacements = table.insert_key(key)
            displacement_arr.append(displacements)
        except MaxDisplacementsExceededError:
            # print(f"Unable to insert key in {table} with load factor {load_factor}")
            displacement_arr.append(max_displacements)

    return displacement_arr


def main():
    for size in TABLE_SIZES:
        for d in D_VALUES:
            for load_factor in LOAD_FACTORS:
                displacement_arr = simulate(d, size, load_factor)
                title = f"size={size}, d={d}, load_factor={load_factor}"
                print(title)

                if len(displacement_arr) != 0:
                    print(f"\tMean: {mean(displacement_arr):.2f}")
                    print(f"\tSTD: {stdev(displacement_arr):.2f}")

                    output_file = Path(f"{OUTPUT_DIR}/{size}/{d}/{load_factor}.png")
                    output_file.parent.mkdir(parents=True, exist_ok=True)

                    plt.plot(sorted(displacement_arr))
                    plt.title(title)
                    plt.xlabel("inserted random keys")
                    plt.ylabel("displacements per insertion")
                    plt.savefig(output_file)
                    plt.close()
                else:
                    break


if __name__ == "__main__":
    main()
