import pygame
import sys

from Unrealistic_Engine.controllers.controller import Controller
from Unrealistic_Engine.utils import utils
from Unrealistic_Engine.views.inventory_view import InventoryView
from Unrealistic_Engine.views.view import View
from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.leaf_node import LeafNode
from Unrealistic_Engine.models.menu import Menu
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine import event_types
from Unrealistic_Engine.models.item import Item
from Unrealistic_Engine.models.armor_item import ArmorItem
from Unrealistic_Engine.models.weapon_item import WeaponItem


class InventoryController(Controller):

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Add Background layer to visible models
        self.view.add_model(
            None, InventoryView.render_background,
            Position(0, 0), View.BACKGROUND)

        # Add Character to visible models
        self.view.add_model(
            self.model.character, InventoryView.render_character_data,
            Position(Map.MAP_SIZE/4, 0), View.FOREGROUND)

        # Build item list from model into a menu
        self.inventory_menu = Menu(self.view, InventoryView.render_inventory_menu,
                                   self.on_node_activated, Position(0, 0))

        for item in self.model.character.inventory.item_list:
            self.inventory_menu.nodes.append(
                LeafNode(item.name, self.select_item, item))

    def handle_key_press(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            if len(Menu.breadcrumbs) > 0:
                self.inventory_menu = self.inventory_menu.go_to_previous_menu()

        if pressed_key == pygame.K_RIGHT or pressed_key == pygame.K_RETURN:
            self.inventory_menu = self.inventory_menu.activate_node()

        if pressed_key == pygame.K_UP:
            self.inventory_menu.dec_active_node()

        if pressed_key == pygame.K_DOWN:
            self.inventory_menu.inc_active_node()

        if pressed_key == pygame.K_i:
            # For now goes back to only game controller, but we need a
            # way to detect previous controller
            self.close_inventory()

    def on_node_activated(self, node):
        if node.is_leaf_node():
            node.execute_action()

    def select_item(self, item):
        if item.slot == Item.Bag:
            # Show a an error that item can't be equipped
            return
        current_loadout = self.model.character.loadout
        if item.slot in current_loadout:
            if item is current_loadout[item.slot]:
                self.unequip_item(item)
            else:
                self.equip_item(item)
        else:
            self.equip_item(item)

    def equip_item(self, item):
        old_item = None
        if item.slot in self.model.character.loadout:
            old_item = self.model.character.loadout[item.slot]
        self.model.character.loadout[item.slot] = item
        # Show dialog that item was equipped

        self.update_stats(old_item, item)

    def unequip_item(self, item):
        del self.model.character.loadout[item.slot]
        self.update_stats(item, None)

    def update_stats(self, old_item, new_item):
        if isinstance(new_item, ArmorItem) or isinstance(old_item, ArmorItem):
            if old_item is not None:
                self.model.character.defense -= old_item.defense_value
            if new_item is not None:
                self.model.character.defense += new_item.defense_value
        elif isinstance(new_item, WeaponItem) or isinstance(old_item, WeaponItem):
            if old_item is not None:
                self.model.character.attack -= old_item.attack_value
            if new_item is not None:
                self.model.character.attack += new_item.attack_value

    def close_inventory(self):
        base = utils.fetch(utils.qualify_controller_name("game_controller"))

        imports = base.GameController.get_imports()

        view_module = utils.fetch(imports[base.GameController.VIEWS]["game_view"])

        view = view_module.GameView()

        controller = base.GameController(self.model, view)

        pygame.event.post(pygame.event.Event(
            event_types.UPDATE_GAME_STATE,
            {"Controller": controller, "View": view}))

    def handle_game_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_game()

    @staticmethod
    def get_imports():
        models = ["map", "trigger"]
        views = ["inventory_view"]
        controllers = ["inventory_controller"]

        return Controller.qualify_imports((models, views, controllers))

    def quit_game(self):
        pygame.quit()
        sys.exit()