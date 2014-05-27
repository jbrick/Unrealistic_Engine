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
<<<<<<< HEAD
        #character = Character(row["Image"])
        character = Character(os.path.join('Images', 'ball.bmp'))
        #TODO: (Sakshi) should load map and images from database instead
        grid_size = 16
        f_image = pygame.image.load(os.path.join('Images', 'tile1.bmp'))
        w_image = pygame.image.load(os.path.join('Images', 'tile2.bmp'))
        game_map = Map(grid_size)
        #Generates preset tile configuration
        for x in range(0, grid_size):
            for y in range(0, grid_size):
                tile = None
                if x == 5:
                    tile = Tile('Floor', f_image)
                elif x % 3 == 0:
                    if y % 3 == 0:
                        tile = Tile('Wall', w_image)
                    else:
                        tile = Tile('Floor', f_image)
                else:
                    if y % 3 == 2:
                        tile = Tile('Wall', w_image)
                    else:
                        tile = Tile('Floor', f_image)
                position = Position(x, y)
                game_map.addOrReplaceTile(tile, position)

        game = Game(character, game_map)
        return game
=======
        character = Character(row["Image"])

        # Game is made up of one map for now.
        cursor = self.__database_execute("SELECT * FROM Maps WHERE Name = 'Basic'", None)
        row = cursor.fetchone()

        # Load the map tiles for this map.
        cursor = self.__database_execute("SELECT TileId, Index_X, Index_Y FROM MapTile WHERE MapId = %d" % row["Id"], None)
        tiles = cursor.fetchall()

        # Load the associated tile images for the map tiles.
        
        # Build a game object.

        # Return a game object.
        return map_list
>>>>>>> Started DB implementation for Maps and Tiles.
