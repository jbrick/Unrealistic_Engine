import sqlite3 as lite
import sys
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

class Database(Model):
    def __init__(self):
        self.db = None

    def load_application(self):
        character = self.__load_characters()
        maps = self.__load_maps()
        game = Game(character, maps)
        return game

    def __database_execute(self, sql, args):
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

    def __load_characters(self):
        # Currently game only consists of one character.
        cursor = self.__database_execute("SELECT * FROM Character", None)
        row = cursor.fetchone()
        character_image = pygame.image.load(
            os.path.join('Images', row['Image']))
        character_image_scaled = pygame.transform.scale(
            character_image, (Character.SIZE, Character.SIZE))
        return Character(character_image_scaled)

    def __load_maps(self):

        maps = {}

        # Game is now made up of multiple maps
        cursor = self.__database_execute(
            "SELECT * FROM Map", None)
        loaded_maps = cursor.fetchall()

        for each_map in loaded_maps:
            game_map = Map(Map.GRID_SIZE)
            # Load the map tiles for this map.
            cursor = self.__database_execute(
                """SELECT mt.TileId, mt.Index_X, mt.Index_Y, t.Name, t.Walkable,
                 t.Image, mt.Id FROM MapTile AS mt JOIN Tile as t
                 ON mt.TileId = t.Id
                WHERE MapId = %d""" % each_map['Id'], None)

            map_tiles = cursor.fetchall()

            # Add all the tiles into the map.
            for row_map_tiles in map_tiles:
                tile_image = pygame.image.load(
                    os.path.join('Images', row_map_tiles['Image']))
                tile_image_scaled = pygame.transform.scale(
                    tile_image, (Tile.SIZE, Tile.SIZE))
                map_tile_id = row_map_tiles['Id']

                # Add trigger for this tile.
                cursor = self.__database_execute(
                    """SELECT Chance, Action_Type, Triggered_On, Action_Data FROM Trigger
                    WHERE MapTileId = %s""" % (map_tile_id), None)

                trigger_row = cursor.fetchone()
                if trigger_row is not None:
                    trigger = Trigger(
                        trigger_row['Chance'],
                        trigger_row['Action_Type'],
                        trigger_row['Triggered_On'],
                        trigger_row['Action_Data'])
                else:
                    trigger = None

                position = Position(
                    row_map_tiles['Index_X'], row_map_tiles['Index_Y'])

                tile = Tile(
                    row_map_tiles['Name'], tile_image_scaled, position,
                    trigger, row_map_tiles['Walkable'])
                
                game_map.addOrReplaceTile(tile)

            maps[each_map['Name']] = game_map

        return maps

    def save_game(self, game_memento):
        cursor = self.__database_execute(
            """INSERT INTO GameState(Name, Current_Map, Character_Position_X, Character_Position_Y)
            VALUES (?, ?, ?, ?)""",
            game_memento.name, game_memento.current_map,
            game_memento.character_memento.position.x_coord,
            game_memento.character_memento.position.y_coord, None)

    def get_saved_games(self):
        cursor = self.__database_execute("SELECT Name FROM GameState", None)
        memento_name_rows = cursor.fetchall()

        memento_names = []
        for row in memento_name_rows:
                memento_names.append(row["Name"])

        return memento_names

    def load_saved_game(self, memento_name):
        cursor = self.__database_execute(
            """SELECT (Current_Map, Character_Position_X, Character_Position_Y) FROM GameState
            WHERE Name = %s""" % memento_name, None)
        memento_row = cursor.fetchone()
        current_map = memento_row['Current_Map']
        character_position = Position(
                memento_row['Character_Position_X'], memento_row['Character_Position_Y'])

        character_memento = CharacterMemento(character_position)
        game_memento = GameMemento(memento_name, current_map, character_memento)

        return game_memento



