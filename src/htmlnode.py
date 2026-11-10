from typing_extensions import final


class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        final_string = ""
        if self.props is None or len(self.props) == 0:
            return final_string
        for prop in self.props:
            attribute = self.props[prop]
            final_string +=(f' {prop}="{attribute}"')
        return final_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        print(self.tag)
        print(self.value)
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        if self.children == None or self.children == []:
            raise ValueError("no children")
        child_tags = ""
        for child in self.children:
            child_tags += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_tags}</{self.tag}>"
