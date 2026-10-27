"""Implement this function, then run: python test_build_order.py --practice"""


def build_order(projects, dependencies):
    # TODO 1: Build an adjacency list and count prerequisites (indegree).
    # TODO 2: Put projects with indegree zero in a deque.
    # TODO 3: Remove one ready project and append it to the result.
    # TODO 4: Reduce its dependents' indegrees; enqueue newly ready projects.
    # TODO 5: Return [] if some projects remain blocked, otherwise the result.
    raise NotImplementedError("Implement the build order algorithm here")


if __name__ == "__main__":
    print(build_order(["app", "database", "config"],
                      [("config", "database"), ("database", "app")]))
