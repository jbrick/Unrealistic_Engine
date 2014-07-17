from Unrealistic_Engine.models.node import Node


class LeafNode(Node):

    def __init__(self, label, action,  *args):
        Node.__init__(self, label)
        self.action_args = args
        self.action = action

    @staticmethod
    def is_leaf_node():
        return True

    def execute_action(self):
        if not self.action_args:
            return self.action()
        else:
            return self.action(*self.action_args)