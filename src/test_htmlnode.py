import unittest
from htmlnode import HTMLNode


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

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "test")
        with self.assertRaises(Exception, msg="Node has no props"):
            node.props_to_html()


if __name__ == "__main__":
    unittest.main()
