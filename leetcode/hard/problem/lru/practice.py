"""Implement the interface, then run test_lru_cache.py --practice."""


class LRUCache:
    def __init__(self, capacity: int):
        # TODO: Validate capacity; create a dictionary and two sentinels.
        raise NotImplementedError

    def get(self, key: int) -> int:
        # TODO: Return -1 for a miss; otherwise move to MRU and return value.
        raise NotImplementedError

    def put(self, key: int, value: int) -> None:
        # TODO: Update existing keys and mark them MRU.
        # For new keys, evict LRU if full, then insert at MRU.
        # A zero-capacity cache stores nothing.
        raise NotImplementedError
