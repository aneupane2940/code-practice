"""LRU cache: dictionary + doubly linked list, O(1) get and put."""


class _Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """Store integer keys/values; evict the least recently used key when full.

    A successful get or any put makes that key most recently used.
    Missing keys return -1. Zero capacity is allowed; negative capacity is not.
    """

    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")
        self.capacity = capacity
        self.nodes = {}  # key -> node for constant-time lookup
        # Sentinels eliminate special cases for empty lists and endpoints.
        self.head = _Node()  # head.next is the least recently used node
        self.tail = _Node()  # tail.prev is the most recently used node
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Unlink an existing data node from its two neighbors."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _append(self, node):
        """Insert a node immediately before tail (the most recent end)."""
        previous = self.tail.prev
        previous.next = node
        node.prev = previous
        node.next = self.tail
        self.tail.prev = node

    def _touch(self, node):
        self._remove(node)
        self._append(node)

    def get(self, key: int) -> int:
        node = self.nodes.get(key)
        if node is None:
            return -1
        self._touch(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        node = self.nodes.get(key)
        if node is not None:
            node.value = value
            self._touch(node)
            return

        if len(self.nodes) == self.capacity:
            oldest = self.head.next
            self._remove(oldest)
            del self.nodes[oldest.key]

        node = _Node(key, value)
        self.nodes[key] = node
        self._append(node)


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    print("get(1):", cache.get(1))  # 10; key 2 is now least recent
    cache.put(3, 30)  # Evicts key 2
    print("get(2):", cache.get(2))  # -1
    cache.put(4, 40)  # Evicts key 1
    print("get(1):", cache.get(1))  # -1
    print("get(3):", cache.get(3))  # 30
    print("get(4):", cache.get(4))  # 40
