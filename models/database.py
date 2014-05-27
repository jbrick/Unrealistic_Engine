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


class Database(Model):
    def __init__(self):
        self.db = None

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

    def load_application(self):
        # Currently game only consists of one character.
        cursor = self.__database_execute("SELECT * FROM Character", None)
        row = cursor.fetchone()
        character_image = pygame.image.load(
            os.path.join('Images', row['Image']))
        character = Character(character_image)

        # Game is made up of one map for now.
        cursor = self.__database_execute(
            "SELECT * FROM Map WHERE Name = 'Basic'", None)
        map_item = cursor.fetchone()
        grid_size = 16
        game_map = Map(grid_size)

        # Load the map tiles for this map.
        cursor = self.__database_execute(
            """SELECT mt.TileId, mt.Index_X, mt.Index_Y, t.Type, t.Image
            FROM MapTile AS mt JOIN Tile as t ON mt.TileId = t.Id
            WHERE MapId = %d""" % map_item['Id'], None)

        map_tiles = cursor.fetchall()

        # Add all the tiles into the map.
        for row_map_tiles in map_tiles:
                tile_image = pygame.image.load(
                    os.path.join('Images', row_map_tiles['Image']))
                tile = Tile(row_map_tiles['Type'], tile_image)
                position = Position(
                    row_map_tiles['Index_X'], row_map_tiles['Index_Y'])
                game_map.addOrReplaceTile(tile, position)

        game = Game(character, game_map)
        return game
