from Unrealistic_Engine.models.node import Node


class LeafNode(Node):

    def __init__ (self, submenu):
        self.submenu = submenu;
