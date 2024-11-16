import unittest
from htmlnode import HTMLNode, NoPropertiesError


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


if __name__ == "__main__":
    unittest.main()
