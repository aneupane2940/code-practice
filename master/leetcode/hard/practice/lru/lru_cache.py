class Node:
    """
    """

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class LRUCache:
    """Cache integer keys and values, evicting the least recently used item."""

    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")

        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add(self, node: Node) -> None:
        prev = self.tail.prev
        prev.next = node

        node.prev = prev
        node.next = self.tail

        self.tail.prev = node

    def _remove(self, node: Node) -> None:
        prev = node.prev

        prev.next = node.next
        node.next.prev = prev

    def _touch(self, node: Node) -> None:
        self._remove(node)
        self._add(node)

    def get(self, key: int) -> int | None:
        node = self.cache.get(key)
        if node is None:
            return None

        self._touch(node)
        return node.value

    def put(self, key: int, value: int) -> int:
        if self.capacity == 0:
            return value

        node = self.cache.get(key)

        if node is not None:
            node.value = value
            self._touch(node)
            return node.value

        if len(self.cache) == self.capacity:
            leftmost = self.head.next
            del self.cache[leftmost.key]
            self._remove(leftmost)

        node = Node(key, value)
        self.cache[key] = node
        self._add(node)

        return node.value


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    print("get(1):", cache.get(1))  # 10; key 2 is now least recent
    cache.put(3, 30)  # Evicts key 2
    print("get(2):", cache.get(2))  # None
    cache.put(4, 40)  # Evicts key 1
    print("get(1):", cache.get(1))  # None
    print("get(3):", cache.get(3))  # 30
    print("get(4):", cache.get(4))  # 40
