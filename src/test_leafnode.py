import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode(None, None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_tag(self):
        node = LeafNode(None, "This is a test!", None)
        self.assertEqual("This is a test!", node.to_html())

    def test_no_props(self):
        node = LeafNode("p", "This is a test!", None)
        self.assertEqual("<p>This is a test!</p>", node.to_html())

    def test_with_props(self):
        node = LeafNode("a", "Google", {"href": "https://www.google.com/"})
        self.assertEqual('<a href="https://www.google.com/">Google</a>', node.to_html())


if __name__ == "__main__":
    unittest.main()
