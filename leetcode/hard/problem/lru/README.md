# LRU Cache — Least Recently Used

## Problem

Implement `LRUCache(capacity)` with two operations:

- `get(key)`: return the stored value, or `-1` if absent. A hit marks the key
  most recently used; a miss changes nothing.
- `put(key, value)`: insert or update a key and mark it most recently used.
  When inserting into a full cache, evict the least recently used key first.

Use integer keys and values. Both operations should take O(1) average time.
Zero capacity stores nothing; negative capacity raises `ValueError`.
No external packages are required.

## Run

From the repository root:

```sh
cd leetcode/hard/problem/lru
../../.venv/bin/python lru_cache.py
../../.venv/bin/python test_lru_cache.py
```

In PyCharm, open `lru_cache.py` and right-click → Run. The example prints
`10, -1, -1, 30, 40`, each with a label.

For practice, implement `practice.py`, then run:

```sh
../../.venv/bin/python test_lru_cache.py --practice
```

Practice tests intentionally fail until you implement the starter.

## Walkthrough (capacity = 2)

Order is shown from **least recent → most recent**.

| Operation | Result | Cache order | Reason |
| --- | --- | --- | --- |
| `put(1, 10)` | — | 1 | New key |
| `put(2, 20)` | — | 1, 2 | New key |
| `get(1)` | 10 | 2, 1 | Access refreshes key 1 |
| `put(3, 30)` | — | 1, 3 | Evict key 2 |
| `get(2)` | -1 | 1, 3 | Miss leaves order unchanged |
| `put(4, 40)` | — | 3, 4 | Evict key 1 |
| `get(1)` | -1 | 3, 4 | Key 1 was evicted |
| `get(3)` | 30 | 4, 3 | Refresh key 3 |
| `get(4)` | 40 | 3, 4 | Refresh key 4 |

## Why a dictionary and a doubly linked list?

The dictionary maps each key directly to its node. A list alone would need a
linear search to find a key. A dictionary alone does not provide explicit
constant-time unlinking and recency ordering for this implementation.

The doubly linked list maintains access order:

```text
head <-> least recent <-> ... <-> most recent <-> tail
```

`head` and `tail` are dummy nodes (sentinels); they never contain cached data.
They make the empty list and endpoint operations work with the same code.
Each real node stores a key, value, previous pointer, and next pointer.
The key is needed to delete the dictionary entry during eviction.

### Moving a node

1. Unlink it: connect its previous neighbor directly to its next neighbor.
2. Insert it just before `tail`: update both of the node's pointers and
   both neighboring pointers.

`get` performs a dictionary lookup and moves a hit to the tail.
`put` updates and moves an existing node, or removes `head.next` when full
before appending a new node. Updating a key never evicts another key.

## Complexity

For capacity C, `get` and `put` take O(1) average time (dictionary operations
are average constant time). Storage is O(C), plus two sentinel nodes.
The cache is intended for sequential use; it does not coordinate threads.

## LRU compared with LFU

LRU evicts the key whose last access happened longest ago. LFU evicts the
key accessed the fewest times, usually breaking ties by recency. A key used
many times earlier can still be evicted by LRU if other keys were used later.

## Common mistakes

- Forgetting to refresh recency when updating an existing key.
- Refreshing order on a failed lookup.
- Removing an evicted node from the list but leaving it in the dictionary.
- Updating only one side of the doubly linked list.
- Evicting a key when an existing key is merely being updated.

Try tracing the pointers on paper, then implement the starter without looking
at the solution. The tests also compare mixed operations with an independent
`OrderedDict` reference model.
