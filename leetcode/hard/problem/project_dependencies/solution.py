"""Run both solutions. Each algorithm lives in its own file."""
from solution_bfs import build_order_bfs
from solution_dfs import build_order_dfs

# Preserve the original entry point for existing callers.
build_order = build_order_bfs


if __name__ == "__main__":
    projects = list("abcdef")
    dependencies = [("a", "d"), ("f", "b"), ("b", "d"), ("f", "a"), ("d", "c")]
    for algorithm in (build_order_bfs, build_order_dfs):
        print(algorithm.__name__, algorithm(projects, dependencies))
