def _build_graph(projects, dependencies):

    graph = {project: [] for project in projects}
    if len(projects) != len(graph):
        raise ValueError("project names must match to unique projects")
    indegree = {project: 0 for project in projects}
    seen = set()
    for prerequisite, dependent in dependencies:
        if prerequisite not in graph or dependent not in graph:
            raise ValueError("prerequisite must exist in graph")
        if (prerequisite, dependent) in seen:
            continue
        seen.add((prerequisite,dependent))
        graph[prerequisite].append(dependent)
        indegree[dependent] +=1
    return graph, indegree
