
import math
from typing import Optional
from abc import ABC, abstractmethod

from utils import get_random_key


class MaxDisplacementsExceededError(Exception):
    """Insertion exceeded the maximum number of displacements."""


class HashTable(ABC):
    """Base HashTable class."""

    def __init__(self, *,
                 size: int,
                 max_displacements: int) -> None:
        self.slots = [None] * size
        self.max_displacements = max_displacements

    @property
    def size(self):
        """Return the size of the hash table."""

        return len(self.slots)

    @property
    def n(self):
        """Return the number of keys in the hash table."""

        return sum(1 for key in self.slots if key is not None)

    @property
    def load_factor(self):
        """Return the load factor of the hash table."""

        return self.n / self.size

    def fill_random(self, target_load_factor: float=1.0) -> None:
        """Reset the table and fill it with random keys to the specified load factor."""

        self.slots = [None] * self.size
        num_keys = math.floor(len(self.slots) * target_load_factor)

        for _ in range(num_keys):
            random_key = get_random_key()
            self.insert_key(random_key)

    @abstractmethod
    def insert_key(self, key) -> int:
        """Insert a key into the hash table.
        Returns the number of displacements needed to insert the key.

        If the insertion failed, raises MaxDisplacementsExceededError.
        """

    def __str__(self):
        return (
            f"HashTable("
            f"size={self.size}, "
            f"max_displacements={self.max_displacements}, "
            f"load_factor={self.load_factor})"
        )
