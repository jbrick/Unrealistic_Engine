from Unrealistic_Engine.models.node import Node


class MenuNode(Node):

    def __init__(self, submenu, label):
        self.submenu = submenu
        self.label = label