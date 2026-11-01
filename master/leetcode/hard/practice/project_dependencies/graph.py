def build_graph(
    projects: list[str],
    dependencies: list[tuple[str, str]],
) -> tuple[dict[str, list[str]], dict[str, int]]:
    """Return adjacency lists and incoming-edge counts.

    Each dependency pair is (prerequisite, dependent).
    Duplicate dependency pairs are ignored.
    """
    graph = {project: [] for project in projects}

    if len(graph) != len(projects):
        raise ValueError("Project names must be unique")

    indegree = {project: 0 for project in projects}
    seen = set()

    for prerequisite, dependent in dependencies:
        if prerequisite not in graph or dependent not in graph:
            raise ValueError(
                f"Dependency ({prerequisite!r}, {dependent!r}) "
                "references an unknown project"
            )
        if (prerequisite, dependent) in seen:
            continue
        seen.add((prerequisite, dependent))
        graph[prerequisite].append(dependent)
        indegree[dependent] += 1

    return graph, indegree
