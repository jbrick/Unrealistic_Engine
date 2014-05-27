class Menu():
    
    __nodeStack = []
    __currentMenu = None
    
    @property
    def nodeCount(self):
        return len(self.nodes)
    
    """
    Constructor.
    """
    def __init__ (self):
        self.nodes = []
        self.activeNode = 0;
        activeicon = pygame.image.load("../img/menu_active.png")
    
    """
    Adds a new menu item to this menu.
    
    @param newNode: The node to be added
    """
    def addItem (self, newNode):
        if (isinstance (newNode, Node)):
            self.nodes.append (newNode)
        else:
            raise TypeError ("You may only add Node objects.")

    """
    Adds a new menu item at a specific index.
    
    @param newNode: The node to be added
    @param index: The point in the menu where the new item will be added
    """
    def addItem (self, newNode, index):
        if (isinstance (newNode, Node)):
            if ((index >= 0) && (index < len (nodes))):
                self.nodes.insert (index, newNode)
                
                if (self.activeNode != None && index < self.activeNode):
                    self.activeNode++
            else:
                raise IndexError ("The given index is out of bounds.")
        else:
           raise TypeError ("You may only add Node objects.")
    
    """
    Removes the given item from the menu.
    
    @param target: Either the menu item to be removed or its position in the list
    """
    def removeItem (self, target):
        if (isinstance (target, (int, float, long)))
            
        elif (isinstance (newNode, Node)):
            # Note that List.remove will generate its own exception if the value is not in the list
            tmp = self.nodes [self.activeNode]
            
            self.nodes.remove (target)
            
            if (tmp != self.nodes [self.activeNode]):
                self.activeNode--
        else:
            raise TypeError ("This function only accepts Node objects or numerics.")

    """
    Makes the target item the selected item.
    
    @param target: Either a reference of the node itself or its position in the menu.
    """
    def selectItem (self, target):
        if (isinstance(target, (int, float, long)):
            if (target >= 0 && target <= len(self.nodes)):
                self.activeNode = target
            else:
                IndexError ("The given index is out of bounds.")
        elif (isinstance (newNode, Node)):
            self.activeNode = self.nodes.index (newNode)
        else:
            raise TypeError ("This function only accepts Node objects or numerics.")
