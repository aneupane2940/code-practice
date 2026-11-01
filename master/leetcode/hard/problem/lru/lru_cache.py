class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LRUCache:
    def __init__(self, capacity:int):
       self.capacity = capacity
       self.head = Node()
       self.tail = Node()
       self.head.next = self.tail
       self.tail.prev = self.head
       self.cache = dict()

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def add(self, node):
        prev = self.tail.prev
        prev.next = node
        node.next = self.tail

        node.prev = prev
        self.tail.prev = node



    def refresh(self, node):
        self.remove(node)
        self.add(node)


    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.refresh(node)
            return node.value
        return None

    def put(self, key, value):
        if self.capacity == 0:
            return""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.refresh(node)
            return node.value

        if len(self.cache) == self.capacity:
            oldest = self.head.next
            self.remove(oldest)
            del self.cache[oldest.key]

        node = Node(key, value)
        self.cache[key] = node
        self.add(node)
        return node.value


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
