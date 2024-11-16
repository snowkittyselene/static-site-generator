from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        # Parent nodes must have a tag
        if self.tag == None:
            raise ValueError

        # Parent nodes must have children
        if self.children == None:
            raise NoChildrenError

        # If passed sanity checks, display as HTML
        html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()
        return html + f"</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, Children: {self.children}, Props: {self.props})"


class NoChildrenError(Exception):
    pass
