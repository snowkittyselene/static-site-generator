import re
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            delimited = node.text.split(delimiter)
            if len(delimited) % 2 == 0:
                raise ValueError("Invalid Markdown syntax")
            for i in range(len(delimited)):
                if delimited[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(delimited[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(delimited[i], text_type))
            new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
