
import math
import random
from typing import Optional

from utils import get_hashing_functions, get_random_key


class RandomWalkHashTable:
    """Random Walk d-ary Cuckoo hash table implementation."""

    def __init__(self,
                 size: int,
                 d: int,
                 max_displacements: int,
                 load_factor: Optional[float] = None) -> None:
        self.size = size
        self.d = d

        self.hashing_functions = get_hashing_functions(self.d)
        self.max_displacements = max_displacements

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


    def insert_key(self, key, dry_run: bool=False) -> tuple[bool, int]:
        """Insert a key into the hash table.
        Returns a pair containing if the key was inserted and the number of displacements.

         If ``dry_run`` is True, simulate the insertion without modifying the hash table.
        """

        table = self.table.copy() if dry_run else self.table
        previous_position = None

        for i in range(self.max_displacements):

            # Try every candidate position
            candidate_positions = self.get_candidate_positions(key, previous_position)

            for pos in candidate_positions:
                if table[pos] is None:
                    table[pos] = key
                    if not dry_run:
                        self.num_elements += 1
                    return True, i

            # Randomly evict one resident
            position = random.choice(candidate_positions)
            table[position], key = key, table[position]

            # Save previous position
            previous_position = position

        return False, self.max_displacements


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

