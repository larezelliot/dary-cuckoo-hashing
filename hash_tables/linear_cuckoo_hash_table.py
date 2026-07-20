from typing import override

from hash_tables.hash_table import HashTable, MaxDisplacementsExceededError
from utils import get_hashing_functions


class LinearCuckooHashTable(HashTable):
    """Linear Cuckoo hash table implementation.

    This is a combination of linear probing that kicks elements if a position is taken,
    then check next position and repeat until an empty space is found.

    This method is created to be able to compared number of displacements in
    a brute force way."""

    def __init__(self, *, size: int, max_displacements: int) -> None:
        super().__init__(size=size, max_displacements=max_displacements)
        self.hash = get_hashing_functions(1)[0]  # HACK

    @override
    def insert_key(self, key) -> int:
        slots = self.slots
        position = self.hash(key) % self.n

        # Start displacements until reaching max_displacement
        for displacement in range(self.max_displacements):

            # Insert in empty space
            if slots[position] is None:
                slots[position] = key
                return displacement

            # Evict current resident if no empty space was found
            slots[position], key = key, slots[position]

            # Move to next position
            position = (position + 1) % self.n

        # Return infinity if max_displacements is reached
        raise MaxDisplacementsExceededError()

    @override
    def __str__(self):
        return (
            f"LinearCuckooHashTable("
            f"size={self.size}, "
            f"load_factor={self.load_factor}, "
            f"max_displacements={self.max_displacements})"
        )
