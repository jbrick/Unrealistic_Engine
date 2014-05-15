import sqlite3 as lite
import sys
from game import Game
from character import Character
from PIL import Image


class Database:
    def __init__(self):
        self.db = None

    def __database_execute(self, sql, args):
        self.db = lite.connect("game.db")
        with self.db:
            self.db.row_factory = lite.Row
            cursor = self.db.cursor()
            if args == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, args)
        return cursor

    def load_application(self):
        cursor = self.__database_execute("SELECT * FROM Character", None)
        row = cursor.fetchone()
        character = Character(row["Image"])
        game = Game(character)
        return game

    def save_character(self, character):
        self.__database_execute(
            "INSERT INTO CHARACTER (Image) VALUES ?", character.image)

    def save_game(self, game):
        save_character(game.character)



db = Database()
app = db.load_application()
im = Image.open(app.character.image)
im.show()