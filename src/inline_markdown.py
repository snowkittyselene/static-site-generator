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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            extracted_images = extract_markdown_images(node.text)
            text = node.text
            for extracted_image in extracted_images:
                # make the node for the image
                image_url = extracted_image[1]
                image_alt = extracted_image[0]
                image_text = f"![{image_alt}]({image_url})"
                image_node = TextNode(image_alt, TextType.IMAGE, image_url)
                split_text = text.split(image_text, 1)
                if split_text[0] != "":
                    split_nodes.append(TextNode(split_text[0], TextType.TEXT))
                split_nodes.append(image_node)
                text = split_text[1]
            new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            extracted_links = extract_markdown_links(node.text)
            text = node.text
            for extracted_link in extracted_links:
                # make the node for the image
                link_url = extracted_link[1]
                link_desc = extracted_link[0]
                link_text = f"[{link_desc}]({link_url})"
                link_node = TextNode(link_desc, TextType.LINK, link_url)
                split_text = text.split(link_text, 1)
                if split_text[0] != "":
                    split_nodes.append(TextNode(split_text[0], TextType.TEXT))
                split_nodes.append(link_node)
                text = split_text[1]
            new_nodes.extend(split_nodes)
    return new_nodes
