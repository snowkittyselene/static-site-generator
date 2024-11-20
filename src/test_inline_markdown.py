import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
)
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

    def test_match_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_match_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_images(self):
        text = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([text]),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_split_links(self):
        text = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([text]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()
