class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        # Can't turn properties to HTML if there are no properties
        if self.props == None:
            raise NoPropertiesError
        html = ""
        for prop in self.props:
            html += f'{prop}="{self.props[prop]}" '
        return html[:-1]

    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"


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

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, props: {self.props})"


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


class NoPropertiesError(Exception):
    pass


class NoChildrenError(Exception):
    pass
