import sys
import pygame
from Unrealistic_Engine import event_types
from Unrealistic_Engine.utils.utils import Utils
from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.views.main_menu import MainMenu
from Unrealistic_Engine.models.node_leaf import LeafNode
from Unrealistic_Engine.models.node_menu import MenuNode
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.database import Database


class MenuController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

        main_menu = Menu()

        main_menu.addItem(LeafNode(Utils.quit, "Quit"))
        model.addItem(LeafNode(Database().save_game(model.create_memento("test")), "Save Game"))
        model.addItem(LeafNode(Database().load_saved_game("test"), "Load Saved Game"))
        //cant do above since LeafNode only takes function pointer.. not atcual function.
            //can be fixed by adding extra arguement for args in function
        // also cant get anything returned --> game memento

        view.add_model(self.model, MainMenu.render_menu, 0, View.BACKGROUND)
        MenuController.activeMenu = main_menu

    @staticmethod
    def get_imports():
        models = ["menu", "node_menu", "node_leaf"]
        views = ["main_menu"]
        controllers = ["menu_controller"]
        
        return Controller.qualify_imports((models, views, controllers))

    @staticmethod
    def build_menu():
        main_menu = Menu()

        main_menu.addItem(LeafNode(Utils.quit, "Quit"))
        return main_menu

    def handle_key_press(self, pressed_key):
        if (pressed_key == pygame.K_LEFT):
            if (len(Menu.breadcrumbs) > 0):
                # Go to previous menu
                self.view.remove_model(self.model)
                self.model = Menu.breadcrumbs.pop();
                self.view.add_model(self.model, MainMenu.render_menu, 0,
                    View.BACKGROUND)
        if (pressed_key == pygame.K_RIGHT or pressed_key == pygame.K_RETURN):
            if (isinstance(self.model.nodes [self.model.activeNode], MenuNode)):
                # Traverse into submenu
                Menu.breadcrumbs.append(self.model)
                self.view.remove_model(self.model)
                self.model = self.model.nodes [self.model.activeNode].submenu
                self.view.add_model(self.model, MainMenu.render_menu, 0,
                    View.BACKGROUND)
            elif (isinstance(self.model.nodes [self.model.activeNode], LeafNode)):
                # Activate action associate with menu item
                self.model.nodes [self.model.activeNode].action()
        if (pressed_key == pygame.K_UP):
            # Previous item in current menu
            self.model.activeNode -= 1
            
            # Default behaviour is to wrap around at the end of the menu
            if (self.model.activeNode < 0):
                self.model.activeNode = (self.model.nodeCount - 1)
        if (pressed_key == pygame.K_DOWN):
            # Next item in current menu
            self.model.activeNode += 1
            
            # Default behaviour is to wrap around at the end of the menu
            if (self.model.activeNode >= self.model.nodeCount):
                self.model.activeNode = 0
        if (pressed_key == pygame.K_ESCAPE):
            base = Utils.fetch(Utils.qualify_controller_name("game_controller"))
            
            imports = base.GameController.get_imports()
            
            view_module = Utils.fetch(imports [base.GameController.VIEWS] ["game_view"])
            
            model = Database().load_application()
            view = view_module.GameView()
            controller = base.GameController(model, view)

            Menu.breadcrumbs = []

            pygame.event.post(pygame.event.Event(
                event_types.UPDATE_GAME_STATE,
                {"Controller": controller, "View": view}))

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
