class Node:
    def __init__(
        self,
        key: int | None = None,
        value: int | None = None,
    ) -> None:
        self.key = key
        self.value = value
        self.next: Node | None = None
        self.prev: Node | None = None
        self.frequency = 1


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def append(self, node: Node) -> None:
        prev = self.tail.prev
        assert prev is not None

        prev.next = node
        node.prev = prev

        node.next = self.tail
        self.tail.prev = node

        self.size += 1

    def remove(self, node: Node) -> None:
        prev = node.prev
        assert prev is not None and node.next is not None

        prev.next = node.next
        node.next.prev = prev

        self.size -= 1

    def pop_lru(self) -> Node | None:
        if self.size == 0:
            return None
        oldest = self.head.next
        assert oldest is not None
        self.remove(oldest)
        return oldest


class LFUCache:
    """Evict the least frequently used key, breaking ties by recency."""

    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("Capacity cannot be negative")
        self.capacity = capacity
        self.nodes_by_key: dict[int, Node] = {}
        self.lists_by_frequency: dict[int, DoublyLinkedList] = {}
        self.min_frequency = 0

    def get(self, key: int) -> int:
        node = self.nodes_by_key.get(key)
        if node is None:
            return -1
        self._increase_frequency(node)
        assert node.value is not None
        return node.value

    def _increase_frequency(self, node: Node) -> None:
        old_frequency = node.frequency
        old_list = self.lists_by_frequency[old_frequency]
        old_list.remove(node)

        # Only advance the minimum when its old bucket becomes empty.
        if old_list.size == 0:
            del self.lists_by_frequency[old_frequency]
            if self.min_frequency == old_frequency:
                self.min_frequency += 1

        node.frequency += 1
        if node.frequency not in self.lists_by_frequency:
            self.lists_by_frequency[node.frequency] = DoublyLinkedList()

        self.lists_by_frequency[node.frequency].append(node)

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        node = self.nodes_by_key.get(key)
        if node is not None:
            node.value = value
            # Updating a key counts as a use, just like get().
            self._increase_frequency(node)
            return

        # Evict the oldest node in the lowest-frequency bucket when full.
        if len(self.nodes_by_key) == self.capacity:
            least_frequent_list = self.lists_by_frequency[self.min_frequency]
            oldest = least_frequent_list.pop_lru()
            assert oldest is not None and oldest.key is not None
            del self.nodes_by_key[oldest.key]
            if least_frequent_list.size == 0:
                del self.lists_by_frequency[self.min_frequency]

        # New keys always start at frequency 1.
        node = Node(key, value)
        self.nodes_by_key[key] = node
        self.min_frequency = 1

        if 1 not in self.lists_by_frequency:
            self.lists_by_frequency[1] = DoublyLinkedList()

        self.lists_by_frequency[1].append(node)


def run_example(
    title: str,
    capacity: int,
    steps: list[tuple[str, tuple[int, ...], int | None, str]],
) -> None:
    """Print LeetCode-style results and explain each operation."""
    print(f"\n{title}")
    cache = LFUCache(capacity)
    outputs = [None]
    print(f"LFUCache({capacity}) -> null: Store at most {capacity} items.")

    for operation, arguments, expected, explanation in steps:
        result = getattr(cache, operation)(*arguments)
        assert result == expected, (
            f"{operation}{arguments}: expected {expected}, got {result}"
        )
        outputs.append(result)
        arguments_text = ", ".join(map(str, arguments))
        result_text = "null" if result is None else str(result)
        print(f"{operation}({arguments_text}) -> {result_text}: {explanation}")

    # LeetCode displays null for constructors and put(), which return no value.
    output_text = ", ".join(
        "null" if result is None else str(result) for result in outputs
    )
    print(f"Output: [{output_text}]")


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
