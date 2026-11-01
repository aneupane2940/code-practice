class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        # Dummy nodes:
        # head <-> ...real nodes... <-> tail
        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

        self.size = 0

    def add(self, node):
        """
        Add node to the end.
        End = most recently used within this frequency.
        """
        prev_node = self.tail.prev

        prev_node.next = node
        node.prev = prev_node

        node.next = self.tail
        self.tail.prev = node

        self.size += 1

    def remove(self, node):
        """Remove a specific node in O(1)."""
        node.prev.next = node.next
        node.next.prev = node.prev

        self.size -= 1

    def remove_lru(self):
        """
        Remove least recently used node.
        LRU node is immediately after head.
        """
        if self.size == 0:
            return None

        node = self.head.next
        self.remove(node)

        return node


class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity

        # key -> Node
        self.key_map = {}

        # frequency -> DoublyLinkedList
        self.freq_map = {}

        # Minimum frequency currently in cache
        self.min_freq = 0


    def _increase_freq(self, node):
        """
        Move node from frequency f
        to frequency f + 1.
        """

        old_freq = node.freq

        # 1. Remove from old frequency list
        old_list = self.freq_map[old_freq]
        old_list.remove(node)

        # 2. Update min_freq if necessary
        if old_freq == self.min_freq and old_list.size == 0:
            self.min_freq += 1

        # 3. Increase frequency
        node.freq += 1
        new_freq = node.freq

        # 4. Create new frequency list if needed
        if new_freq not in self.freq_map:
            self.freq_map[new_freq] = DoublyLinkedList()

        # 5. Add node as MRU of new frequency
        self.freq_map[new_freq].add(node)


    def get(self, key: int) -> int:

        # Key doesn't exist
        if key not in self.key_map:
            return -1

        node = self.key_map[key]

        # Access increases frequency
        self._increase_freq(node)

        return node.value


    def put(self, key: int, value: int) -> None:

        # Edge case
        if self.capacity == 0:
            return

        # --------------------------------
        # CASE 1: Key already exists
        # --------------------------------

        if key in self.key_map:
            node = self.key_map[key]

            # Update value
            node.value = value

            # put() counts as usage
            self._increase_freq(node)

            return

        # --------------------------------
        # CASE 2: New key
        # --------------------------------

        # Cache full -> evict LFU
        if len(self.key_map) >= self.capacity:

            # Get DLL corresponding to minimum frequency
            min_freq_list = self.freq_map[self.min_freq]

            # Among same frequency, remove LRU
            node_to_remove = min_freq_list.remove_lru()

            # Remove from key map
            del self.key_map[node_to_remove.key]

        # Create new node
        new_node = Node(key, value)

        # Every new node starts with frequency 1
        if 1 not in self.freq_map:
            self.freq_map[1] = DoublyLinkedList()

        self.freq_map[1].add(new_node)

        # Add to key map
        self.key_map[key] = new_node

        # New node has frequency 1,
        # therefore minimum frequency is now 1
        self.min_freq = 1


def run_example(title, capacity, steps):
    """Print LeetCode-style results and explain each operation."""
    print(f"\n{title}")
    cache = LFUCache(capacity)
    outputs = [None]
    print(f"LFUCache({capacity}) -> null: Store at most {capacity} items.")

    for operation, arguments, expected, explanation in steps:
        result = getattr(cache, operation)(*arguments)
        assert result == expected, f"{operation}{arguments}: expected {expected}, got {result}"
        outputs.append(result)
        arguments_text = ", ".join(map(str, arguments))
        result_text = "null" if result is None else str(result)
        print(f"{operation}({arguments_text}) -> {result_text}: {explanation}")

    # LeetCode displays null for constructors and put(), which return no value.
    print("Output: [" + ", ".join("null" if x is None else str(x) for x in outputs) + "]")


if __name__ == "__main__":
    print("LFU evicts the least frequently used key.")
    print("If frequencies tie, evict the least recently used key.")
    print("New keys start at frequency 1; get() and updating put() increase it.")

    run_example("Example 1: LeetCode LFU Cache example", 2, [
        ("put", (1, 1), None, "Insert key 1 with frequency 1."),
        ("put", (2, 2), None, "Insert key 2 with frequency 1."),
        ("get", (1,), 1, "Return 1; key 1 now has frequency 2."),
        ("put", (3, 3), None, "Evict key 2 (frequency 1); insert key 3."),
        ("get", (2,), -1, "Key 2 was evicted, so return -1."),
        ("get", (3,), 3, "Return 3; keys 1 and 3 now both have frequency 2."),
        ("put", (4, 4), None, "Frequencies tie; evict key 1, used less recently than key 3."),
        ("get", (1,), -1, "Key 1 was evicted, so return -1."),
        ("get", (3,), 3, "Return 3; key 3 now has frequency 3."),
        ("get", (4,), 4, "Return 4; key 4 now has frequency 2."),
    ])

    run_example("Example 2: Updating an existing key (extra practice)", 2, [
        ("put", (1, 10), None, "Insert key 1 with frequency 1."),
        ("put", (2, 20), None, "Insert key 2 with frequency 1."),
        ("put", (1, 100), None, "Change key 1's value to 100 and increase its frequency to 2."),
        ("put", (3, 30), None, "Evict key 2 because its frequency is lower than key 1's."),
        ("get", (1,), 100, "Return the updated value 100; frequency becomes 3."),
        ("get", (2,), -1, "Key 2 was evicted."),
        ("get", (3,), 30, "Return 30; frequency becomes 2."),
    ])

    run_example("Example 3: Zero capacity (extra practice)", 0, [
        ("put", (1, 1), None, "Capacity is zero, so nothing is stored."),
        ("get", (1,), -1, "Key 1 is absent, so return -1."),
    ])
