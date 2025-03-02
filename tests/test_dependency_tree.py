import unittest
from treecut.dependency_tree import TreeNode

class TestTreeNode(unittest.TestCase):

    def setUp(self):
        """Set up a sample tree before each test."""
        self.root = TreeNode("ROOT")
        self.n1 = TreeNode("1")
        self.n2 = TreeNode("2")
        self.n3 = TreeNode("3")
        self.n4 = TreeNode("4")
        self.root.add_child(self.n1)
        self.n1.add_child(self.n2)
        self.n1.add_child(self.n3)
        self.n2.add_child(self.n4)

    def test_get_all_edges_dfs(self):
        """Test BFS edge retrieval."""
        expected = [("2", "4")]
        self.assertEqual(self.n2.get_all_edges(dfs=True), expected)

    def test_get_all_edges_bfs(self):
        """Test DFS edge retrieval."""
        expected = [[('ROOT', '1'), ('1', '2'), ('1', '3'), ('2', '4')], [('ROOT', '1'), ('1', '3'), ('1', '2'), ('2', '4')]]
        self.assertIn(self.root.get_all_edges(), expected)

    def test_get_ancestors(self):
        """Test ancestor retrieval."""
        self.assertEqual(self.n4.get_ancestors(), ["2", "1", "ROOT"])
        self.assertEqual(self.n2.get_ancestors(), ["1", "ROOT"])
        self.assertEqual(self.n3.get_ancestors(), ["1", "ROOT"])
        self.assertEqual(self.n1.get_ancestors(), ["ROOT"])
        self.assertEqual(self.root.get_ancestors(), [])

if __name__ == "__main__":
    unittest.main()
