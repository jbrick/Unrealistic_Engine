import sqlite3 as lite
import pygame
import os

from Unrealistic_Engine.utils.position import Position
from Unrealistic_Engine.models.game import Game
from Unrealistic_Engine.models.character import Character
from Unrealistic_Engine.models.model import Model
from Unrealistic_Engine.models.map import Map
from Unrealistic_Engine.models.tile import Tile
from Unrealistic_Engine.models.trigger import Trigger
from Unrealistic_Engine.models.mementos.character import CharacterMemento
from Unrealistic_Engine.models.mementos.game import GameMemento
from Unrealistic_Engine.models.item import Item
from Unrealistic_Engine.models.armor_item import ArmorItem
from Unrealistic_Engine.models.healing_item import HealingItem
from Unrealistic_Engine.models.weapon_item import WeaponItem


class Database(Model):

    # Use Borg design pattern to share game state across any Database instance.
    __shared_state = {"game": None}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.db = None

    def load_application(self):
        if self.game:
            return self.game
        else:
            character = self._load_characters()
            maps = self._load_maps()
            enemies = self._load_enemies()
            items = self._load_items()
            game = Game(character, maps, enemies, items, maps["tower_floor1"])
            self.game = game
            return game

    def _database_execute(self, sql, args):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, "game.db")
        self.db = lite.connect(filename)
        with self.db:
            self.db.row_factory = lite.Row
            cursor = self.db.cursor()
            if args is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, args)
        return cursor

    def _load_characters(self):
        # Currently game only consists of one character.
        cursor = self._database_execute("SELECT * FROM Character WHERE Name = 'Player'", None)
        row = cursor.fetchone()
        return Character(row['Name'], row['Image'], row['Health'],
                         row['Attack'], row['Defense'])

    def _load_enemies(self):
        cursor = self._database_execute("SELECT * FROM Character WHERE Name != 'Player'", None)
        enemies = cursor.fetchall()
        enemy_dict = {}
        for enemy in enemies:
            enemy_image = character_image = pygame.image.load(
                os.path.join('Images', enemy['Image']))
            enemy_image_scaled = pygame.transform.scale(
                enemy_image, (Character.SIZE, Character.SIZE))
            enemy_dict[enemy['Name']] = Character(enemy['Name'], enemy_image_scaled,
                                                  enemy['Health'], enemy['Attack'], enemy['Defense'])

        return enemy_dict

    def _load_items(self):
        cursor = self._database_execute("SELECT * FROM Item", None)
        items = cursor.fetchall()
        item_dict = {}
        types = self.create_types_dict()
        for item in items:
            item_init = types[item['Type']]
            item_dict[item['Name']] = item_init(item['Id'], item['Name'], item['Description'],
                                                item['Slot'], item['Modifier'])
        return item_dict

    def _load_maps(self):

        maps = {}

        # Game is now made up of multiple maps
        cursor = self._database_execute(
            "SELECT * FROM Map", None)
        loaded_maps = cursor.fetchall()

        for each_map in loaded_maps:
            game_map = Map(Map.GRID_SIZE, each_map["Name"], each_map["Music"])
            
            # Load the map layers of this map
            cursor = self._database_execute(
                 """SELECT ID, Layer FROM MapLayer WHERE MapId = %s""" % each_map['Id'], None)
            load_layers = cursor.fetchall()

            for each_layer in load_layers:
                # Load the map tiles for this map.
                cursor = self._database_execute(
                    """SELECT mt.TileId, mt.Index_X, mt.Index_Y, t.Name, t.Walkable,
                     t.Image, mt.Id FROM MapTile AS mt JOIN Tile as t
                     ON mt.TileId = t.Id
                    WHERE MapLayerId = %d""" % each_layer['Id'], None)

                map_tiles = cursor.fetchall()

                # Add all the tiles into the map.
                for row_map_tiles in map_tiles:
                    tile_image = pygame.image.load(
                        os.path.join('Images', row_map_tiles['Image']))
                    tile_image_scaled = pygame.transform.scale(
                        tile_image, (Tile.SIZE, Tile.SIZE))
                    map_tile_id = row_map_tiles['Id']

                    # Add trigger for this tile.
                    cursor = self._database_execute(
                        """SELECT Chance, Action_Type, Triggered_On,
                        Direction_Facing, One_Time, Action_Data FROM
                        Trigger WHERE MapTileId = %s""" % map_tile_id, None)

                    trigger_row = cursor.fetchone()
                    if trigger_row is not None:
                        trigger = Trigger(
                            trigger_row['Chance'],
                            trigger_row['Action_Type'],
                            trigger_row['Triggered_On'],
                            trigger_row['Direction_Facing'],
                            trigger_row['One_Time'],
                            trigger_row['Action_Data'])
                    else:
                        trigger = None

                    position = Position(
                        row_map_tiles['Index_X'], row_map_tiles['Index_Y'])

                    tile = Tile(
                        row_map_tiles['Name'], tile_image_scaled, position,
                        trigger, row_map_tiles['Walkable'])

                    if (each_layer["Layer"] == "Layer1"):
                        game_map.add_or_replace_tile(0, tile)
                    else:
                        game_map.add_or_replace_tile(1, tile)

            maps[each_map['Name']] = game_map

        return maps

    def save_game(self, game_memento):
        cursor = self._database_execute(
            "INSERT INTO GameState(Current_Map, Character_Position_X, Character_Position_Y, "
            "Character_Health, Character_Total_Health, Character_Attack, Character_Defense) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (game_memento.map_name,
             game_memento.character_memento.position.x_coord,
             game_memento.character_memento.position.y_coord,
             game_memento.character_memento.health,
             game_memento.character_memento.total_health,
             game_memento.character_memento.attack,
             game_memento.character_memento.defense))

        game_state_id = cursor.lastrowid
        item_list = game_memento.character_memento.item_list
        loadout = game_memento.character_memento.loadout
        for item in item_list:
            is_equipped = 0
            if item.slot in loadout:
                if loadout[item.slot].name == item.name:
                    is_equipped = 1
            cursor = self._database_execute(
                "INSERT INTO InventoryState(Game_State_ID, Item_ID, Equipped, Quantity)"
                "VALUES (?, ?, ?, ?)",
                (game_state_id, item.item_id, is_equipped, item_list[item])
            )

    def save_game_overwrite(self, saved_game_id, game_memento):
        cursor = self._database_execute(
            "UPDATE GameState SET Current_Map='%s', Character_Position_X='%s', "
            "Character_Position_Y='%s', Character_Health='%s', Character_Total_Health='%s',"
            "Character_Attack='%s', Character_Defense='%s' WHERE Id='%s'" % (game_memento.map_name,
            game_memento.character_memento.position.x_coord,
            game_memento.character_memento.position.y_coord,
            game_memento.character_memento.health,
            game_memento.character_memento.total_health,
            game_memento.character_memento.attack,
            game_memento.character_memento.defense,
            saved_game_id), None)

        cursor = self._database_execute(
            "DELETE FROM InventoryState WHERE Game_State_ID = '%s'" % saved_game_id, None
        )

        item_list = game_memento.character_memento.item_list
        loadout = game_memento.character_memento.loadout
        for item in item_list:
            is_equipped = 0
            if item.slot in loadout:
                if loadout[item.slot].name == item.name:
                    is_equipped = 1
            cursor = self._database_execute(
                "INSERT INTO InventoryState(Game_State_ID, Item_ID, Equipped, Quantity)"
                "VALUES (?, ?, ?, ?)",
                (saved_game_id, item.item_id, is_equipped, item_list[item])
            )

    def get_saved_games(self):
        cursor = self._database_execute("SELECT Id FROM GameState", None)
        memento_name_rows = cursor.fetchall()

        memento_names = []
        for row in memento_name_rows:
                memento_names.append(row["Id"])

        return memento_names

    def load_saved_game(self, memento_id, *args, **kwargs):
        cursor = self._database_execute(
            "SELECT Current_Map, Character_Position_X, Character_Position_Y, Character_Health, "
            "Character_Total_Health, Character_Attack, Character_Defense FROM GameState WHERE Id = %s" % memento_id,
            None)
        memento_row = cursor.fetchone()
        current_map = memento_row['Current_Map']
        character_position = Position(
            memento_row['Character_Position_X'], memento_row['Character_Position_Y'])

        cursor = self._database_execute(
            "SELECT * FROM InventoryState JOIN Item on InventoryState.Item_ID = Item.Id "
            "WHERE InventoryState.Game_State_Id = '%s'" % memento_id, None
        )
        items = cursor.fetchall()
        item_dict = {}
        loadout = {}
        types = self.create_types_dict()
        for item in items:
            item_init = types[item['Type']]
            new_item = item_init(item['Id'], item['Name'], item['Description'],
                                 item['Slot'], item['Modifier'])

            if item['Equipped'] == 1:
                loadout[item['Slot']] = new_item
            item_dict[new_item] = item['Quantity']

        character_memento = CharacterMemento(character_position,
                                             memento_row['Character_Health'],
                                             memento_row['Character_Total_Health'],
                                             memento_row['Character_Attack'],
                                             memento_row['Character_Defense'],
                                             item_dict,
                                             loadout)
        game_memento = GameMemento(current_map, character_memento)

        return game_memento

    def create_types_dict(self):
        return {Item.Weapon: WeaponItem, Item.Armor: ArmorItem, Item.Healing: HealingItem}
