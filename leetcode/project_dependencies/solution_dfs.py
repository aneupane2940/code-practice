"""Topological sorting using recursive depth-first search."""
from graph import _build_graph


def build_order_dfs(projects, dependencies):
    """Use recursive depth-first search and reverse finishing order.

    A project currently on the recursion path signals a cycle if revisited.
    Very deep dependency chains may exceed Python's recursion limit; use BFS
    for those inputs.
    """
    graph, _ = _build_graph(projects, dependencies)
    unvisited, visiting, finished = 0, 1, 2
    state = {project: unvisited for project in projects}
    order = []

    def visit(project):
        if state[project] == visiting:
            return False  # Back edge: a cycle on the current DFS path.
        if state[project] == finished:
            return True  # Shared dependent already processed; not a cycle.

        state[project] = visiting
        for dependent in graph[project]:
            if not visit(dependent):
                return False
        state[project] = finished
        order.append(project)  # All dependents finish before this project.
        return True

    for project in projects:  # Include disconnected and independent projects.
        if not visit(project):
            return []
    order.reverse()  # Prerequisites must appear before their dependents.
    return order


if __name__ == "__main__":
    projects = list("abcdef")
    dependencies = [("a", "d"), ("f", "b"), ("b", "d"), ("f", "a"), ("d", "c")]
    print("DFS build order:", build_order_dfs(projects, dependencies))
    print("Cycle:", build_order_dfs(["a", "b"], [("a", "b"), ("b", "a")]))
