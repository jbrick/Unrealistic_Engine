class Saveable():

    def __init__(self):
        pass

    def create_memento(self):
        raise NotImplementedError("Please Implement this method")

    def set_memento(self, memento):
        raise NotImplementedError("Please Implement this method")