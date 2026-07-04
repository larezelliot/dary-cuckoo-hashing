
import math
import random

from utils import get_hashing_functions, get_random_key


class RandomWalkHashTable:
    """Random Walk d-ary Cuckoo hash table implementation."""

    def __init__(self,
                 size: int,
                 load_factor: float,
                 d: int,
                 max_displacements: int) -> None:
        self.size = size
        self.hashing_functions = get_hashing_functions(d)
        self.max_displacements = max_displacements

        self.table = [None] * self.size
        self.fill(load_factor)


    def get_candidate_positions(self, key) -> list[int]:
        """Return a list of candidate positions for a key."""

        return [h_i(key) % self.size for h_i in self.hashing_functions]


    def insert_key(self, key, dry_run: bool=False) -> tuple[bool, int]:
        """Insert a key into the hash table.
        Returns a pair containing if the key was inserted and the number of displacements.

         If ``dry_run`` is True, simulate the insertion without modifying the hash table.
        """

        table = self.table.copy() if dry_run else self.table

        for i in range(self.max_displacements):

            # Try every candidate position
            candidate_positions = self.get_candidate_positions(key)

            for pos in candidate_positions:
                if table[pos] is None:
                    table[pos] = key
                    return True, i

            # Randomly evict one resident
            pos = random.choice(candidate_positions)
            table[pos], key = key, table[pos]

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

        num_elements = sum(1 for key in self.table if key is not None)
        return num_elements / self.size

