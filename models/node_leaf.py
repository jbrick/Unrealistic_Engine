from Unrealistic_Engine.models.node import Node


class LeafNode(Node):

    def __init__ (self, action, label):
        self.action = action
        self.label = label

    # def act (self):
    #     self.action.execute ()
