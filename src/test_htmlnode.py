import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("a", "test", props={"href": "https://www.google.com"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("a", "test", props={"href": "https://www.google.com"})
        self.assertEqual(
            "HTMLNode(Tag: a, Value: test, Children: None, Props: {'href': 'https://www.google.com'})",
            repr(node),
        )

    def test_props_to_htmL(self):
        node = HTMLNode(
            "a", "test", props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            'href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "test")
        with self.assertRaises(NoPropertiesError):
            node.props_to_html()

    def test_values(self):
        node = HTMLNode("a", "test", props={"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://www.google.com"})


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
