from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        # Leaf nodes must have a value
        if self.value == None:
            raise ValueError

        # If no tag, then display just as raw text
        if self.tag == None:
            return self.value

        if self.props != None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
