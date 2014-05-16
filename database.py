import sqlite3 as lite
import sys
from game import Game
from character import Character
from model import Model


class Database(Model):
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
        # Currently game only consists of one character.
        cursor = self.__database_execute("SELECT * FROM Character", None)
        row = cursor.fetchone()
        character = Character(row["Image"])
        game = Game(character)
        return game
