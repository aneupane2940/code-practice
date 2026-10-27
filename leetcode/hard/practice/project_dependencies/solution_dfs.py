"""Topological sorting using recursive depth-first search."""
from graph import _build_graph


def build_order_dfs(projects, dependencies):

   graph,_ = _build_graph(projects, dependencies)
   unvisited, visiting, finished = 0,1,2

   state = {project: unvisited for project in projects}

   order = []

   def visit(project):
       if state[project] == visiting:
           return False
       if state[project] == finished:
           return True

       state[project] = visiting
       for dependent in graph[project]:
           if not visit(dependent):
               return False

       state[project] = finished
       order.append(project)
       return True

   for project in projects:
       if not visit(project):
           return []

   order.reverse()

   return order


if __name__ == "__main__":
    projects = list("abcdef")
    dependencies = [("a", "d"), ("f", "b"), ("b", "d"), ("f", "a"), ("d", "c")]
    print("DFS build order:", build_order_dfs(projects, dependencies))
    print("Cycle:", build_order_dfs(["a", "b"], [("a", "b"), ("b", "a")]))
