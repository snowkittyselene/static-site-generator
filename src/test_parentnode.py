import unittest
from parentnode import ParentNode, NoChildrenError
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2"),
                LeafNode("li", "Item 3"),
            ],
        )
        self.assertEqual(
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>", node.to_html()
        )

    def test_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2"),
                LeafNode("li", "Item 3"),
            ],
        )

        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_children(self):
        node = ParentNode("div", None)

        with self.assertRaises(NoChildrenError):
            node.to_html()

    def test_parent_as_only_child(self):
        node = ParentNode(
            "div",
            [ParentNode("ul", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2")])],
        )
        self.assertEqual(
            "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>", node.to_html()
        )

    def test_nested_child_no_tag(self):
        node = ParentNode("div", [ParentNode(None, [LeafNode(None, "foo")])])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_nested_child_parentnode_with_no_children(self):
        node = ParentNode("div", [ParentNode("div", None)])
        with self.assertRaises(NoChildrenError):
            node.to_html()

    def test_child_with_no_tag(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Here are some words. "),
                LeafNode(
                    "a", "And here is a link!", {"href": "https://www.google.com"}
                ),
                LeafNode(None, " And some more text!"),
            ],
        )
        self.assertEqual(
            '<p>Here are some words. <a href="https://www.google.com">And here is a link!</a> And some more text!</p>',
            node.to_html(),
        )


if __name__ == "__main__":
    unittest.main()
