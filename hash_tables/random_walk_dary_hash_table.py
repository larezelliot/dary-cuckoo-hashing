
import random
from typing import override

from hash_tables.hash_table import HashTable, MaxDisplacementsExceededError
from utils import get_hashing_functions


class RandomWalkDaryHashTable(HashTable):
    """Random Walk d-ary Cuckoo hash table implementation."""

    def __init__(self, *,
                 size: int,
                 d: int,
                 max_displacements: int,
                 partitioned: bool = False) -> None:
        super().__init__(size=size, max_displacements=max_displacements)

        self.partitioned = partitioned
        self.hashing_functions = get_hashing_functions(d)

    @property
    def d(self):
        """Return the number of hashing functions."""

        return len(self.hashing_functions)

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

    @override
    def insert_key(self, key) -> int:
        slots = self.slots
        previous_position = None

        # Start displacements until reaching max_displacement
        for displacement in range(self.max_displacements):
            candidate_positions = self.get_candidate_positions(key, previous_position)

            # Try every candidate position to find an empty space
            for pos in candidate_positions:
                # Insert in empty space
                if slots[pos] is None:
                    slots[pos] = key
                    return displacement

            # Randomly evict one resident if no empty space was found
            position = random.choice(candidate_positions)
            slots[position], key = key, slots[position]

            # Save position of previously evicted key
            previous_position = position

        # Raises an exception if max_displacements is reached
        raise MaxDisplacementsExceededError()

    @override
    def __str__(self):
        return (
            f"RandomWalkDaryHashTable("
            f"size={self.size}, "
            f"d={self.d}, "
            f"load_factor={self.load_factor}, "
            f"max_displacements={self.max_displacements}, "
            f"partitioned={self.partitioned})"
        )
