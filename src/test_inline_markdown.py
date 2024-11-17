import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestConverter(unittest.TestCase):
    def test_no_text_node(self):
        node = TextNode("I am bold text!", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node, new_nodes[0])

    def test_text_node(self):
        node = TextNode("I am **bold** text!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("I am ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text!", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_closing_delimiter(self):
        node = TextNode("I am **bold text!", TextType.TEXT)
        with self.assertRaises(ValueError, msg="Invalid Markdown syntax"):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_delimiters(self):
        node = TextNode("This is **bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
