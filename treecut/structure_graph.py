"""
To make composite item names
"""

class StructureGraph:
    def __init__(self):
        # Dictionary to store the directed graph with its children
        self.graph = {}

    def add_node(self, node):
        # Add a new node to the graph if it does not already exist
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, source_node, target_node):
        # Ensure both nodes exist in the graph
        self.add_node(source_node)
        self.add_node(target_node)

        # no repeated edges
        if target_node not in self.graph[source_node]:
            self.graph[source_node].append(target_node)

    def display_graph(self):
        # Print each node and its neighbors
        for node, neighbors in self.graph.items():
            print(f"{node}: {', '.join(map(str, neighbors))}")

    def get_all_edges(self):
        ans = []
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                ans.append((node, neighbor))
        return ans