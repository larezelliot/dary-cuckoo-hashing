"""CSE6041"""

from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt
from config import D_VALUES, LOAD_FACTORS, N, OUTPUT_DIR, PARTITIONED_HASH_TABLE, TABLE_SIZES


from hash_tables.hash_table import MaxDisplacementsExceededError
from hash_tables.random_walk_dary_hash_table import RandomWalkDaryHashTable
from utils import get_random_key


def simulate(d: int, table_size: int, load_factor: float):
    max_displacements = table_size * 2

    table = RandomWalkDaryHashTable(size=table_size,
                                    d=d,
                                    max_displacements=max_displacements,
                                    partitioned=PARTITIONED_HASH_TABLE)

    try:
        table.fill_random(load_factor)
    except MaxDisplacementsExceededError:
        print(f"Unable to create {table} with load factor {load_factor}")
        return []  #HACK

    original_slots = table.slots.copy()

    # Create random keys and insert in the table, counting the number of displacements
    random_keys = (get_random_key() for _ in range(N))
    displacement_arr = []

    for key in random_keys:
        # Revert the hash table to original value
        table.slots = original_slots.copy()

        # Attempt to insert into the table
        try:
            displacements = table.insert_key(key)
            displacement_arr.append(displacements)
        except MaxDisplacementsExceededError:
            # print(f"Unable to insert key in {table} with load factor {load_factor}")
            displacement_arr.append(max_displacements)

    return displacement_arr


def save_displacement_plot(displacement_arr: list[int], title, filename):
    mean_value = mean(displacement_arr)
    std_value = stdev(displacement_arr)

    print(f"\tMean: {mean_value:.2f}")
    print(f"\tSTD: {std_value:.2f}")

    output_file = Path(f"{OUTPUT_DIR}/{filename}")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.plot(sorted(displacement_arr))
    plt.title(title)
    plt.xlabel("inserted random keys")
    plt.ylabel("displacements per insertion")
    plt.savefig(output_file)
    plt.close()


def main():
    for size in TABLE_SIZES:
        for d in D_VALUES:
            for load_factor in LOAD_FACTORS:
                title = f"size={size}, d={d}, load_factor={load_factor}"
                displacement_arr = simulate(d, size, load_factor)


                if len(displacement_arr) != 0:
                    print(title)

                    filename = f"{size}/{d}/{load_factor}.png"
                    save_displacement_plot(displacement_arr, title, filename)
                else:
                    print(f"FAILED: {title}")
                    break


if __name__ == "__main__":
    main()
