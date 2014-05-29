import sqlite3 as lite
import csv
import sys
import os
import optparse

def main():
    reader = csv.reader(open(sys.argv[1], "rb"), delimiter=',')
    
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "../../models/game.db")
    db = lite.connect(filename)
    with db:
        cursor = db.cursor()
        # Clear DB of existing tables (focused on one map right now)
        cursor.execute("DROP TABLE IF EXISTS Map")
        cursor.execute("DROP TABLE IF EXISTS Tile")
        cursor.execute("DROP TABLE IF EXISTS MapTile")
        cursor.execute("DROP TABLE IF EXISTS Character")
        
        # Create tables (again if dropped before)
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

        # Insert default character entry
        cursor.execute(
            "INSERT INTO Character (Image) VALUES (?)",
            ["ball.bmp"])

        # Insert default map entry
        cursor.execute(
            "INSERT INTO Map (Name) VALUES (?)",
            ["Basic"])
        #Insert default tiles
        cursor.execute(
            "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
            ("Floor", "tile1.bmp"))
        cursor.execute(
            "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
            ("Wall", "tile2.bmp"))

        cur_row = 0
        for row in reader:
            cur_col = 0
            for entry in row:
                insert_into_maptile(cursor, entry, cur_col, cur_row)
                cur_col += 1

            cur_row += 1

    



#def insert_into_map():


#def insert_into_tile():


def insert_into_maptile(cursor, tile_id, x_pos, y_pos):
    cursor.execute(
        "INSERT INTO MapTile (MapId, TileId, Index_X, Index_Y) VALUES (?, ?, ?, ?)",
        (1, tile_id, x_pos, y_pos))

if __name__ == "__main__":
    main()