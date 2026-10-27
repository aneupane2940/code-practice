# LeetCode practice

Each exercise has its own folder:

```text
leetcode/hard/problem/
    lfu/
        lfu_cache.py
    lru/
        README.md
        lru_cache.py
        practice.py
        test_lru_cache.py
    project_dependencies/
        README.md
        graph.py
        solution.py
        solution_bfs.py
        solution_dfs.py
        practice.py
        test_build_order.py
```

Practice code lives separately in `leetcode/hard/practice/`.

- [LFU cache](hard/problem/lfu/lfu_cache.py): least frequently used eviction.
- [LRU cache](hard/problem/lru/README.md): least recently used eviction.
- [Project dependencies](hard/problem/project_dependencies/README.md): BFS and DFS build order.

In PyCharm, open a solution file and right-click → Run.
From the repository root:

```sh
.venv/bin/python leetcode/hard/problem/lfu/lfu_cache.py
.venv/bin/python leetcode/hard/problem/lru/lru_cache.py
.venv/bin/python leetcode/hard/problem/project_dependencies/solution.py
```

Run tests from the repository root:

```sh
.venv/bin/python leetcode/hard/problem/lru/test_lru_cache.py
.venv/bin/python leetcode/hard/problem/project_dependencies/test_build_order.py
```
