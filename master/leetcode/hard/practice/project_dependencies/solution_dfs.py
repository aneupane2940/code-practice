"""Topological sorting using recursive depth-first search."""

from leetcode.hard.practice.project_dependencies.graph import build_graph

UNVISITED = 0
VISITING = 1
COMPLETED = 2


def build_order_dfs(
    projects: list[str],
    dependencies: list[tuple[str, str]],
) -> list[str]:
    """Return a valid build order, or [] if a cycle exists.

    Each dependency pair is (prerequisite, dependent).
    """
    graph, _ = build_graph(projects, dependencies)
    order = []
    state = {project: UNVISITED for project in projects}

    def dfs(project: str) -> bool:
        if state[project] == VISITING:
            return False
        if state[project] == COMPLETED:
            return True
        state[project] = VISITING

        for dependent in graph[project]:
            if not dfs(dependent):
                return False

        state[project] = COMPLETED
        order.append(project)  # All dependents finish before this project.
        return True

    for project in projects:
        if not dfs(project):
            return []

    order.reverse()
    return order


if __name__ == "__main__":
    projects = list("abcdef")
    dependencies = [("a", "d"), ("f", "b"), ("b", "d"), ("f", "a"), ("d", "c")]
    print("DFS build order:", build_order_dfs(projects, dependencies))
    print("Cycle:", build_order_dfs(["a", "b"], [("a", "b"), ("b", "a")]))
