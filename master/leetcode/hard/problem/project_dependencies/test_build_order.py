"""Checks valid orders without requiring one specific order."""
import sys
import unittest

if "--practice" in sys.argv:
    sys.argv.remove("--practice")
    from practice import build_order
else:
    from solution import build_order


class BuildOrderTests(unittest.TestCase):
    algorithm = staticmethod(build_order)

    def setUp(self):
        self.build_order = self.algorithm

    def check_order(self, projects, dependencies):
        order = self.build_order(projects, dependencies)
        self.assertEqual(set(order), set(projects))
        self.assertEqual(len(order), len(projects))
        positions = {project: index for index, project in enumerate(order)}
        for prerequisite, dependent in dependencies:
            self.assertLess(positions[prerequisite], positions[dependent])

    def test_example(self):
        self.check_order(list("abcdef"), [("a", "d"), ("f", "b"),
                         ("b", "d"), ("f", "a"), ("d", "c")])

    def test_independent(self):
        self.check_order(["app", "docs", "tests"], [])

    def test_duplicate_dependency(self):
        self.check_order(["a", "b"], [("a", "b"), ("a", "b")])

    def test_empty(self):
        self.assertEqual(self.build_order([], []), [])

    def test_cycle(self):
        self.assertEqual(self.build_order(["a", "b"], [("a", "b"), ("b", "a")]), [])

    def test_self_cycle(self):
        self.assertEqual(self.build_order(["a"], [("a", "a")]), [])

    def test_cycle_with_independent_project(self):
        self.assertEqual(self.build_order(list("abc"), [("a", "b"), ("b", "a")]), [])

    def test_unknown_project(self):
        with self.assertRaises(ValueError):
            self.build_order(["a"], [("a", "missing")])

    def test_duplicate_project(self):
        with self.assertRaises(ValueError):
            self.build_order(["a", "a"], [])


if "--practice" not in sys.argv and build_order.__module__ != "practice":
    from solution import build_order_bfs, build_order_dfs

    class BFSBuildOrderTests(BuildOrderTests):
        algorithm = staticmethod(build_order_bfs)

    class DFSBuildOrderTests(BuildOrderTests):
        algorithm = staticmethod(build_order_dfs)


if __name__ == "__main__":
    unittest.main()
