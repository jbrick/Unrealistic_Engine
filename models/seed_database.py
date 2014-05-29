import sqlite3 as lite
import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, "game.db")
db = lite.connect(filename)
with db:
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Map")
    cursor.execute("DROP TABLE IF EXISTS Tile")
    cursor.execute("DROP TABLE IF EXISTS MapTile")
    cursor.execute("DROP TABLE IF EXISTS Character")

    cursor.execute(
        "CREATE TABLE Map"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT)")
    
    cursor.execute(
        "CREATE TABLE Tile"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT, Image TEXT)")

    cursor.execute(
        "CREATE TABLE MapTile"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, MapId INTEGER, TileId INTEGER, Index_X INTEGER, Index_Y INTEGER)")
   
    cursor.execute(
        "CREATE TABLE Character"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Image TEXT)")

    cursor.execute(
        "INSERT INTO Character (Image) VALUES (?)",
        ["ball.bmp"])

    cursor.execute(
        "INSERT INTO Map (Name) VALUES (?)",
        ["Basic"])

    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("Floor", "tile1.bmp"))

    cursor.execute(
        "INSERT INTO MapTile (MapId, TileId, Index_X, Index_Y) VALUES (?, ?, ?, ?)",
        (1, 1, 0, 0))

    cursor.execute(
        "INSERT INTO MapTile (MapId, TileId, Index_X, Index_Y) VALUES (?, ?, ?, ?)",
        (1, 1, 0, 1))
