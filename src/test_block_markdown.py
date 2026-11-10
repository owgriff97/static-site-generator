import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block
from textnode import TextNode, TextType


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocktype_header(self):
        input = "# This is a header."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.HEADING)

    def test_blocktype_header2(self):
        input = "## This is a header."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.HEADING)

    def test_blocktype_header3(self):
        input = "### This is a header."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.HEADING)

    def test_blocktype_header4(self):
        input = "#### This is a header."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.HEADING)

    def test_blocktype_header5(self):
        input = "##### This is a header."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.HEADING)

    def test_blocktype_header6(self):
        input = "###### This is a header."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.HEADING)

    def test_blocktype_header7(self):
        input = "####### This is a header."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_code(self):
        input = "```\nThis is a code block.```"
        type = block_to_block(input)
        self.assertEqual(type, BlockType.CODE)

    def test_blocktype_code_no_end(self):
        input = "```\nThis is a code block.`"
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_code_no_start(self):
        input = "```This is a code block.```"
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_quote(self):
        input = "> This is \n> a quote."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.QUOTE)

    def test_blocktype_quote_no_symbol(self):
        input = "> This is \n a quote."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_quote_one_line(self):
        input = "> This is a quote."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.QUOTE)

    def test_blocktype_unordered(self):
        input = "- This is \n- a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_blocktype_unordered_no_symbol(self):
        input = "- This is \n a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_unordered_no_space(self):
        input = "- This is \n-a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_unordered_one_line(self):
        input = "- This is a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_blocktype_ordered(self):
        input = "1. This is \n2. a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.ORDERED_LIST)

    def test_blocktype_ordered_no_symbol(self):
        input = " This is \n2. a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_ordered_no_space(self):
        input = "1.This is \n2. a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_ordered_late_start(self):
        input = "2. This is \n3. a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_blocktype_ordered_jump(self):
        input = "1. This is \n5. a list."
        type = block_to_block(input)
        self.assertEqual(type, BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()
