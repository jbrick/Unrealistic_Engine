import sqlite3 as lite
import csv
import sys
import os
import optparse


def main():

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "../../models/game.db")
    db = lite.connect(filename)
    with db:
        cursor = db.cursor()

        if sys.argv[1] == "reset":
            reset_database(cursor)
        elif sys.argv[1] == "show":
            show_map_names(cursor)
        elif sys.argv[1] == "create":
            #TODO: check that valid input was given (Notnull, with .csv on end)
            create_map(cursor, sys.argv[2])
        elif sys.argv[1] == "update":
            update_map(cursor, sys.argv[2])
        elif sys.argv[1] == "help":
            print_options()
        else:
            print("Input not valid. ")
            print_options()


def create_map(cursor, map_arg):
    reader = csv.reader(open(map_arg, "rb"), delimiter=',')

    map_name = map_arg
    if map_name.endswith(".csv"):
        map_name = map_name[:-4]
    insert_map(cursor, map_name)
    map_id = get_map_id(cursor, map_name)

    cur_row = 0
    for row in reader:
        cur_col = 0
        for entry in row:
            insert_maptile(cursor, map_id, entry, cur_col, cur_row)
            cur_col += 1
        cur_row += 1
    print("Map with name '%s' was successfully created." % map_name)


def update_map(cursor, map_arg):
    reader = csv.reader(open(map_arg, "rb"), delimiter=',')

    map_name = map_arg
    if map_name.endswith(".csv"):
        map_name = map_name[:-4]

    map_id = get_map_id(cursor, map_name)
    if map_id is None:
        print("There is no map with name '%s'. " +
              "Please use create option instead." % map_name)
        return

    # Removes all current MapTiles with the found map id
    delete_map_tiles(cursor, map_id)

    #Re-adds updated MapTIles
    cur_row = 0
    for row in reader:
        cur_col = 0
        for entry in row:
            insert_maptile(cursor, map_id, entry, cur_col, cur_row)
            cur_col += 1
        cur_row += 1
    print("Map with name '%s' was successfully updated." % map_name)


def delete_map_tiles(cursor, map_id):
    cursor.execute(
        "DELETE FROM MapTile WHERE MapId = %s" % map_id)


def populate_tile_table(cursor):
    #TODO: write function to import tiles rather than staticly type here
    # 1
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("Grass", "rpggrass.png"))
    # 2
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("Dirt", "rpgdirt.png"))
    # 3
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("WaterTopLeft", "water-top-left.png"))
    # 4
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("WaterTopRight", "water-top-right.png"))
    # 5
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("WaterBottomLeft", "water-bottom-left.png"))
    # 6
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("WaterBottomRight", "water-bottom-right.png"))
    # 7
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("WaterSolid", "water-solid.png"))
    # 8
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("BrickBeige", "brick-beige.png"))
    # 9
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("BrickBlue", "brick-blue.png"))
    # 10
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("BrickBrown", "brick-brown.png"))
    # 11
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("StairsUp", "stairs-up.png"))
    # 12
    cursor.execute(
        "INSERT INTO Tile (Type, Image) VALUES (?, ?)",
        ("StairsDown", "stairs-down.png"))


def insert_map(cursor, map_name):
    cursor.execute(
        "INSERT INTO Map (Name) VALUES (?)",
        [map_name])


def get_map_id(cursor, map_name):
    result = cursor.execute(
                "SELECT ID FROM Map WHERE NAME = '%s'"
                % map_name)
    for row in result:
        return row[0]


def insert_maptile(cursor, map_id, tile_id, x_pos, y_pos):
    cursor.execute(
        "INSERT INTO MapTile (MapId, TileId, Index_X, Index_Y) VALUES (?, ?, ?, ?)",
        (map_id, tile_id, x_pos, y_pos))


def show_map_names(cursor):
    result = cursor.execute(
                "SELECT * FROM Map")
    for row in result:
        print("Name: '%s', ID: '%s'" % (row[1], row[0])) 


def reset_database(cursor):
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

    # Insert default data
    # Insert default character entry
    cursor.execute(
        "INSERT INTO Character (Image) VALUES (?)",
        ["ranger_m.png"])
    # Insert default map entry
    cursor.execute(
        "INSERT INTO Map (Name) VALUES (?)",
        ["Basic"])
    # Insert default tiles
    populate_tile_table(cursor)

    print("Database successfully reset to base data.")


def print_options():
    print("To use the map creation utility, use one of the following commands:")
    print("     show - prints out the name and id of every map in the DB")
    print("     reset - drops all tables in the DB and recreates them with the base data.")
    print("     create <map_name>.csv - creates a map from the given data in the passed in csv file")
    print("     update <map_name>.csv - updates a map that already exists from the given data in the passed in csv file")

if __name__ == "__main__":
    main()