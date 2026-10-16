def _build_graph(projects, dependencies):
    """Validate input and create prerequisite -> dependent edges."""
    graph = {project: [] for project in projects}
    if len(graph) != len(projects):
        raise ValueError("Project names must be unique")
    indegree = {project: 0 for project in projects}
    seen = set()
    for prerequisite, dependent in dependencies:
        if prerequisite not in graph or dependent not in graph:
            raise ValueError("Dependency references an unknown project")
        if (prerequisite, dependent) in seen:
            continue
        seen.add((prerequisite, dependent))
        graph[prerequisite].append(dependent)
        indegree[dependent] += 1
    return graph, indegree


