"""Topological sorting using BFS (Kahn's algorithm)."""

from collections import deque

from leetcode.hard.practice.project_dependencies.graph import build_graph


def build_order_bfs(
    projects: list[str],
    dependencies: list[tuple[str, str]],
) -> list[str]:
    """Return a valid build order, or [] if a cycle exists.

    Each dependency pair is (prerequisite, dependent).
    """
    graph, indegree = build_graph(projects, dependencies)

    ready = deque(project for project in projects if indegree[project] == 0)
    order = []

    while ready:
        node = ready.popleft()
        order.append(node)

        for dependent in graph[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)

    return order if len(order) == len(projects) else []


if __name__ == "__main__":
    projects = list("abcdef")
    dependencies = [("a", "d"), ("f", "b"), ("b", "d"), ("f", "a"), ("d", "c")]
    print("BFS build order:", build_order_bfs(projects, dependencies))
    print("Cycle:", build_order_bfs(["a", "b"], [("a", "b"), ("b", "a")]))
