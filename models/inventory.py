class Inventory():

    def __init__(self, item_list):
        self.item_list = item_list

    def add_item(self, item):
        if item in self.item_list:
            self.item_list[item] += 1
            return
        self.item_list[item] = 1

    def remove_item(self, item):
        if self.item_list[item] > 1:
            self.item_list[item] -= 1
        else:
            del self.item_list[item]
