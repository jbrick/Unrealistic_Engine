from Unrealistic_Engine.models.node import Node


class LeafNode(Node):

    def __init__ (self, action, name):
        self.action = action;
        self.name = name;

    # def act (self):
    #     self.action.execute ();
