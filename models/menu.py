import pygame
import os

from Unrealistic_Engine.models.node import Node


class Menu():

    breadcrumbs = []
    
    @property
    def nodeCount(self):
        return len(self.nodes)
    
    """
    Constructor.
    """
    def __init__(self):
        self.nodes = []
        self.activeNode = 0;
        self.activeIcon = pygame.image.load(os.path.join("Images",
            "menu_active.png"))

    """
    Adds a new menu item to this menu.
    
    @param newNode: The node to be added
    """
    def addItem(self, newNode):
        if isinstance(newNode, Node):
            self.nodes.append(newNode)
        else:
            raise TypeError ("You may only add Node objects.")

    """
    Adds a new menu item at a specific index.
    
    @param newNode: The node to be added
    @param index: The point in the menu where the new item will be added
    """
    def insertItem(self, newNode, index):
        if isinstance(newNode, Node):
            self.nodes.insert(index, newNode)
            
            if index <= self.activeNode:
                self.activeNode += 1
        else:
           raise TypeError("You may only add Node objects.")
    
    """
    Removes the given item from the menu.
    
    @param target: Either the item to be removed or its position in the list
    """
    def removeItem(self, target):
        if isinstance(target, (int, float, long)):
            self.nodes.remove(target)
        elif isinstance(target, Node):
            tmp = self.nodes [self.activeNode]
            
            self.nodes.remove(target)
            
            if tmp != self.nodes[self.activeNode]:
                self.activeNode -= 1
        else:
            raise TypeError("This function only accepts Node objects or numerics.")

    """
    Makes the target item the selected item.
    
    @param target: Either a reference of the node or its position in the menu.
    """
    def selectItem(self, target):
        if isinstance(target, (int, float, long)):
            self.activeNode = target
        elif isinstance(target, Node):
            self.activeNode = self.nodes.index(target)
        else:
            raise TypeError("This function only accepts Node objects or numerics.")
