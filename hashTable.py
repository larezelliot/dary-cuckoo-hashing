
import math
import random
from typing import Optional

from utils import get_hashing_functions, get_random_key


class MaxDisplacementsExceededError(Exception):
    """Insertion exceeded the maximum number of displacements."""


class RandomWalkDaryHashTable:
    """Random Walk d-ary Cuckoo hash table implementation."""

    def __init__(self,
                 size: int,
                 d: int,
                 max_displacements: Optional[int] = None,
                 partitioned: bool = False) -> None:
        self.partitioned = partitioned
        self.max_displacements = max_displacements or size

        self.table = [None] * size
        self.hashing_functions = get_hashing_functions(d)

    @property
    def size(self):
        """Return the size of the hash table."""

        return len(self.table)

    @property
    def d(self):
        """Return the number of hashing functions."""

        return len(self.hashing_functions)

    @property
    def n(self):
        """Return the number of keys in the hash table."""

        return sum(1 for key in self.table if key is not None)

    @property
    def load_factor(self):
        """Return the load factor of the hash table."""

        return self.n / self.size


    def get_candidate_positions(self, key, previous_pos = None) -> list[int]:
        """Return a list of candidate positions for a key.

        If the previous position was given, remove from candidates.


        HACK: If the partition behaviour is used, behave with a similar approach of using
        d separate tables of size m/d to avoid visiting previous_pos after being cuckoo-ed out.
        This was used in the d-cuckoo paper experiments.
        """

        if self.partitioned:
            sub_size = self.size // self.d
            positions = [i * sub_size + h_i(key) % sub_size
                        for i, h_i in enumerate(self.hashing_functions)]
            if previous_pos is not None:
                positions.remove(previous_pos)
        else:
            positions = [h_i(key) % self.size
                        for h_i in self.hashing_functions]

        return positions


    def insert_key(self, key) -> int:
        """Insert a key into the hash table.
        Returns the number of displacements needed to insert the key.

        If the insertion failed, raises MaxDisplacementsExceededError.
        """
        table = self.table
        previous_position = None

        # Start displacements until reaching max_displacement
        for displacement in range(self.max_displacements):
            candidate_positions = self.get_candidate_positions(key, previous_position)

            # Try every candidate position to find an empty space
            for pos in candidate_positions:
                # Insert in empty space
                if table[pos] is None:
                    table[pos] = key
                    return displacement

            # Randomly evict one resident if no empty space was found
            position = random.choice(candidate_positions)
            table[position], key = key, table[position]

            # Save position of previously evicted key
            previous_position = position

        # Return infinity if max_displacements is reached
        raise MaxDisplacementsExceededError()


    def fill_random(self, target_load_factor: float=1.0) -> None:
        """Reset the table and fill it with random keys to the specified load factor."""

        self.table = [None] * self.size
        num_keys = math.floor(len(self.table) * target_load_factor)

        for _ in range(num_keys):
            random_key = get_random_key()
            self.insert_key(random_key)


    def __str__(self):
        return (
            f"RandomWalkDaryHashTable("
            f"size={self.size}, "
            f"d={self.d}, "
            f"load_factor={self.load_factor}, "
            f"max_displacements={self.max_displacements}, "
            f"paritioned={self.partitioned})"
        )