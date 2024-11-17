import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.google.com")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.google.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual("TextNode(This is a text node, bold, None)", repr(node))

    def test_convert_to_html_normal(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            "LeafNode(None, This is a text node, props: None)", repr(html_node)
        )

    def test_convert_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            "LeafNode(b, This is a text node, props: None)", repr(html_node)
        )

    def test_convert_to_html_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            "LeafNode(i, This is a text node, props: None)", repr(html_node)
        )

    def test_convert_to_html_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            "LeafNode(code, This is a text node, props: None)", repr(html_node)
        )

    def test_convert_to_html_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://www.google.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            "LeafNode(a, This is a link, props: {'href': 'http://www.google.com/'})",
            repr(html_node),
        )

    def test_convert_to_html_image(self):
        node = TextNode(
            "This is an image", TextType.IMAGE, "https://i.redd.it/138zreuhs3lc1.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            "LeafNode(img, None, props: {'src': 'https://i.redd.it/138zreuhs3lc1.png', 'alt': 'This is an image'})",
            repr(html_node),
        )

    def test_convert_to_html_invalid_type(self):
        node = TextNode("Test", "test")
        with self.assertRaises(Exception, msg="Invalid text type"):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
