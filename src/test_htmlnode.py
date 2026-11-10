import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_no_props(self):
        node = HTMLNode(None, None, None, None)
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_one_prop(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_two_props(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_value(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node_1 = LeafNode("span", "child")
        child_node_2 = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_brother(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        brother_node = LeafNode("span", "brother")
        parent_node = ParentNode("div", [child_node, brother_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><span>brother</span></div>",
        )

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("p", "great_grandchild")
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><p>great_grandchild</p></b></span></div>",
        )

    def test_to_html_with_parent_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node], {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span href="https://www.google.com"><b>grandchild</b></span></div>',
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children(self):
        parent_node = ParentNode("span", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children(self):
        parent_node = ParentNode("span", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()
