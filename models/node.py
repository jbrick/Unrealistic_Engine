import uuid


class Node():

    def __init__(self, label):
        self.label = label

        # Give every node a unique id so we can reference it by id.
        self.id = uuid.uuid4()

    @staticmethod
    def is_leaf_node():
        return False

