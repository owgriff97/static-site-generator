from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from block_markdown import BlockType, block_to_block, markdown_to_blocks
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links, text_to_text_nodes
from enum import Enum

def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_text_nodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children

def paragraph_spacing(block: str) -> str:
    lines = block.split("\n")
    new_block = " ".join(lines)
    return new_block

def header_count(block: str) -> tuple[int, str]:
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    text = block[count + 1:]
    return (count, text)

def quote_strip(block: str) -> str:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_line = line[1:]
        new_lines.append(new_line.lstrip())
    new_block = " ".join(new_lines)
    return new_block

def u_list_format(block: str) -> list[HTMLNode]:
    lines = block.split("\n")
    new_list = []
    for line in lines:
        new_line = line[2:]
        new_line = text_to_children(new_line)
        list_item = ParentNode("li", new_line, None)
        new_list.append(list_item)
    return new_list

def o_list_format(block: str) -> list[HTMLNode]:
    lines = block.split("\n")
    new_list = []
    for line in lines:
        count = 0
        for char in line:
            if char != ".":
                count += 1
            else:
                count += 1
                break
        new_line = line[count + 1:]
        new_line = text_to_children(new_line)
        list_item = ParentNode("li", new_line, None)
        new_list.append(list_item)
    return new_list

def code_to_html(block: str) -> list[HTMLNode]:
    block = block[4:-3]
    code_node = TextNode(block, TextType.CODE, None)
    code_node = [text_node_to_html_node(code_node)]
    return code_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        type = block_to_block(block)
        if type == BlockType.PARAGRAPH:
            paragraph_node = ParentNode("p", text_to_children(paragraph_spacing(block)), None)
            children.append(paragraph_node)
        elif type == BlockType.HEADING:
            level, text = header_count(block)
            heading_node = ParentNode(f"h{level}", text_to_children(text), None)
            children.append(heading_node)
        elif type == BlockType.QUOTE:
            quote_node = ParentNode("blockquote", text_to_children(quote_strip(block)), None)
            children.append(quote_node)
        elif type == BlockType.UNORDERED_LIST:
            unordered_node = ParentNode("ul", u_list_format(block), None)
            children.append(unordered_node)
        elif type == BlockType.ORDERED_LIST:
            ordered_node = ParentNode("ol", o_list_format(block), None)
            children.append(ordered_node)
        elif type == BlockType.CODE:
            code_node = ParentNode("pre", code_to_html(block), None)
            children.append(code_node)
    final_html = ParentNode("div", children, None)
    return final_html
