# Project dependencies: build order

A CodeSignal-style practice exercise, also commonly called Build Order.
No external packages are required.

## Problem

You have project names and dependency pairs. Return an order in which every
project can be built. A pair `(a, b)` means **a must be built before b**.
Include projects that have no dependencies. If a circular dependency makes a
complete build impossible, return `[]`. Multiple orders may be valid.

Project names are unique strings. Raise `ValueError` for duplicate project
names or dependencies referencing unknown projects. Ignore repeated edges.
An empty project list returns `[]`.

Example:

```text
projects = [a, b, c, d, e, f]
dependencies = [(a,d), (f,b), (b,d), (f,a), (d,c)]
One valid result: [e, f, b, a, d, c]
```

## Run and learn

From the repository root (use `python3` if your terminal calls Python that):

```sh
cd leetcode/project_dependencies
python solution.py
python test_build_order.py
```

In PyCharm, open either file, right-click, and select Run.

1. Read the problem and implement `build_order` in `practice.py`.
2. Run `python test_build_order.py --practice` to check your implementation.
   These tests will fail until you finish the starter.
3. Compare your implementation with `solution.py`.

## How the solution works

Draw each dependency as an arrow from prerequisite to dependent.
The indegree of a project counts its unfinished prerequisites.
Start a queue with all projects whose indegree is zero. Build one project,
then subtract one from the indegree of each dependent. Whenever a dependent
reaches zero, add it to the queue. Repeat until the queue is empty.

For the example, the initial ready queue is `[e, f]`. Building `e` unlocks
nothing. Building `f` unlocks `b` and `a`. After both build, `d` becomes ready;
then building `d` unlocks `c`.

If fewer projects were built than supplied, a cycle blocked the remaining
projects. For example, `a -> b -> a` has no possible starting point.

Time: O(V + E). Space: O(V + E), where V is the number of projects and E
is the number of dependency pairs.

Try next: return buildable groups that can run in parallel, or report the
projects left blocked by a cycle.

## BFS and DFS in separate files

- `solution_bfs.py`: Kahn's algorithm, using a queue and indegrees.
- `solution_dfs.py`: recursive DFS, using unvisited/visiting/finished states.
- `graph.py`: shared input validation and graph construction.
- `solution.py`: runs both examples; `build_order` still defaults to BFS.

```sh
python solution_bfs.py
python solution_dfs.py
python test_build_order.py
```

DFS follows each project's dependents before recording that project. Reversing
this finishing order puts prerequisites first. Revisiting a project marked
`visiting` detects a cycle; revisiting a `finished` project is safe.
Both algorithms take O(V + E) time and space. Recursive DFS can hit Python's
recursion limit on very long chains; BFS avoids that limitation.
Different valid orders from BFS and DFS are expected.
