import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)
from htmlnode import ParentNode, LeafNode


class TestMarkdownBlocks(unittest.TestCase):
    def test_split_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block\n* This is a list item\n* This is another list item""",
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_to_html(self):
        markdown = """# Header

Paragraph

- List item
- List item

1. List item
2. List item

[link](somewhere)

![image](something)

*italics*

**bold**"""
        expected = ParentNode(
            "div",
            [
                LeafNode("h1", "Header"),
                LeafNode("p", "Paragraph"),
                ParentNode(
                    "ul", [LeafNode("li", "List item"), LeafNode("li", "List item")]
                ),
                ParentNode(
                    "ol", [LeafNode("li", "List item"), LeafNode("li", "List item")]
                ),
                LeafNode("a", "link", {"href": "somewhere"}),
                LeafNode("img", None, {"src": "something", "alt": "image"}),
                LeafNode("i", "italics"),
                LeafNode("b", "bold"),
            ],
        )
        self.assertEqual(markdown_to_html_node(markdown), expected)


if __name__ == "__main__":
    unittest.main()
