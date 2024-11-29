from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    return [split_block.strip() for split_block in split_blocks if split_block != ""]


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        for i in range(1, len(lines) + 1):
            if not lines[i - 1].startswith(f"{i}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        blocks.append(block_to_html_node(block))
    return ParentNode("div", html_nodes)


def block_to_html_node(block):
    match block_to_block_type(block):
        case BlockType.HEADING:
            return header_to_html_node(block)
        case BlockType.CODE:
            return LeafNode("code", block)
        case BlockType.QUOTE:
            return LeafNode("blockquote", block)
        case BlockType.UNORDERED_LIST:
            return list_to_html_node(block, "ul")
        case BlockType.ORDERED_LIST:
            return list_to_html_node(block, "ol")
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case _:
            raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))


def header_to_html_node(header):
    header_number = header.count("#")
    text = header.strip("#").strip()
    return LeafNode(f"h{header_number}", text)


def list_to_html_node(list, type):
    children = []
    lines = list.split("\n")
    for line in lines:
        children.append(LeafNode("li", line.split(" ", 1)[1]))
    return ParentNode(type, children)
