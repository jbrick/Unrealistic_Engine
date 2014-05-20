class Menu():
    
    """
    Root menu type. Should be subclassed into menus for specific functions
    - Inventory
    - Pause *
        - For now this will be the only implementation
    - Battle
    """
    """
    Required attributes for menu
        - List of Nodes
            - Nodes may be leaf nodes or menu nodes
                - Leaf nodes will be defined with an action
                - Menu nodes will be defined with a child menu 
        - Pointer to the active node
    """
    
    def addItem (newNode):
        # Push the given node onto the node list
    
    def removeItem (target):
        # Remove target from node list if it exists
