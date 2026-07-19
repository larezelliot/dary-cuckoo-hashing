
import math
import random
from typing import Optional

from utils import get_hashing_functions, get_optimal_max_displacements, get_random_key


class RandomWalkHashTable:
    """Random Walk d-ary Cuckoo hash table implementation."""

    def __init__(self,
                 size: int,
                 d: int,
                 load_factor: Optional[float] = None) -> None:
        self.size = size  # TODO: size might change!
        self.d = d

        self.hashing_functions = get_hashing_functions(self.d)
        self.table = [None] * self.size
        self.num_elements = 0

        if load_factor:
            self.fill(load_factor)


    def get_candidate_positions(self, key, previous_pos = None) -> list[int]:
        """Return a list of candidate positions for a key.

        If the previous position was given, remove from candidates."""

        # TODO: regular position calculation without using previous position
        # positions = [h_i(key) % self.size for h_i in self.hashing_functions]

        # HACK: This is a similar approach of using d separate tables
        # of size m/d to avoid visiting previous_pos after being cuckoo-ed out.
        # This was used in the d-cuckoo paper experiments.
        sub_size = self.size // self.d
        positions = [i * sub_size + h_i(key) % sub_size
                     for i, h_i in enumerate(self.hashing_functions)]

        if previous_pos is not None:
            positions.remove(previous_pos)

        return positions


    def insert_key(self, key) -> tuple[int, int]:
        """Insert a key into the hash table.
        Returns the number of total displacements and rehashes.
        """
        table = self.table
        previous_position = None
        max_displacements = get_optimal_max_displacements(self.num_elements, self.size)

        for i in range(max_displacements):
            # Try every candidate position
            candidate_positions = self.get_candidate_positions(key, previous_position)
            for pos in candidate_positions:
                if table[pos] is None:
                    table[pos] = key
                    self.num_elements += 1
                    return i, 0

            # Randomly evict one resident
            position = random.choice(candidate_positions)
            table[position], key = key, table[position]

            # Save previous position
            previous_position = position

        # If unable to find an empty position, rehash and insert
        rehash_d, rehash_r = self.rehash()
        d, r = self.insert_key(key)
        return rehash_d + d, rehash_r + r


    def rehash(self) -> tuple[int, int]:
        """Rebuild the table using new hash functions.

        Return the number of displacements and rehashes completed"""

        keys = [key for key in self.table if key is not None]

        # Empty the old tabl
        self.hashing_functions = get_hashing_functions(self.d)
        self.table = [None] * self.size
        self.num_elements = 0

        # Insert keys keeping track of displacements and sub-rehashes
        displacements = 0
        rehashes = 1
        for key in keys:
            d, r = self.insert_key(key)

            displacements += d
            rehashes += r

        # HACK: Validate that all the keys match the current number or elements
        assert len(keys) == self.num_elements

        return displacements, rehashes


    def fill(self, load_factor: float=1.0) -> None:
        """Reset the table and fill it with random keys to the specified load factor."""

        self.table = [None] * self.size
        num_elements = math.floor(len(self.table) * load_factor)

        for _ in range(num_elements):
            random_key = get_random_key()
            inserted, _ = self.insert_key(random_key)

            if not inserted:
                raise Exception(f"Unable to fill table of size {self.size} with a load factor of {load_factor}. " +
                                f"Stopped at {self.calculate_load_factor()}")


    def calculate_load_factor(self):
        """Calculate and return the load factor in the table"""

        return self.num_elements / self.size

