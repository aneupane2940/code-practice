"""Topological sorting using BFS (Kahn's algorithm)."""
from collections import deque
from graph import _build_graph


def build_order_bfs(projects, dependencies):
    """Use a queue of ready projects; return [] if a cycle blocks completion.

    Each (prerequisite, dependent) pair means prerequisite must build first.
    Project names must be unique strings. Unknown dependencies raise ValueError.
    """
    graph, indegree = _build_graph(projects, dependencies)

    # A project with no unfinished prerequisites can build immediately.
    ready = deque(project for project in projects if indegree[project] == 0)
    order = []
    while ready:
        project = ready.popleft()
        order.append(project)
        for dependent in graph[project]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)

    # Any unprocessed projects are blocked by a cycle.
    return order if len(order) == len(projects) else []


if __name__ == "__main__":
    projects = list("abcdef")
    dependencies = [("a", "d"), ("f", "b"), ("b", "d"), ("f", "a"), ("d", "c")]
    print("BFS build order:", build_order_bfs(projects, dependencies))
    print("Cycle:", build_order_bfs(["a", "b"], [("a", "b"), ("b", "a")]))
