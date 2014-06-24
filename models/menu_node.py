from Unrealistic_Engine.models.node import Node


class MenuNode(Node):

    def __init__(self, label):
        Node.__init__(self, label)
        self.submenu = None
