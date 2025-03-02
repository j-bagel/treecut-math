"""
The class for the tree structure of math problems
"""

from collections import deque

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def get_all_edges(self, dfs = False) -> list:
        if dfs:
            # get all edges starting from self as root, using DFS
            ans = []
            stack = [self]

            while stack:
                node = stack.pop()
                for child in node.children:
                    ans.append((node.name, child.name))
                    stack.append(child)

            return ans
        else:
            # BFS by default
            ans = []
            q = deque([self])

            while q:
                node = q.popleft()
                for child in node.children:
                    ans.append((node.name, child.name))
                    q.append(child)

            return ans


    def get_ancestors(self) -> list:
        # the first element is parent.name, the last is 'ROOT'
        node = self
        ans = []
        while node.parent is not None:
            ans.append(node.parent.name)
            node = node.parent
        return ans
