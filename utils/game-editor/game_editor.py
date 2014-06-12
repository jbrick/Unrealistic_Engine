import sqlite3 as lite
import csv
import sys
import os
import json
import argparse

from Unrealistic_Engine.models.trigger import Trigger
from Unrealistic_Engine.models.map import Map


def main():
    parser = argparse.ArgumentParser(
        description="Utility to create games in unrealistic engine")

    parser.add_argument(
        "--reset", dest="to_run", action="store_const", 
        const=reset_database, default=None,
        help="Resets the game database to default state")

    parser.add_argument(
        "--show_map_names", dest="to_run", action="store_const", 
        const=show_map_names, default=None,
        help="Displays the names of all loaded maps")

    parser.add_argument(
        "--create_map", dest="to_run", action="store_const", 
        const=create_maps, default=None,
        help="Creates a map using a passed in .csv file")

    parser.add_argument(
        "--update_map", dest="to_run", action="store_const", 
        const=update_map, default=None,
        help="Updates a map using a passed in .csv file")

    parser.add_argument(
        "--add_tileset", dest="to_run", action="store_const", 
        const=add_tilesets, default=None,
        help="Adds a .json defined tileset to the game")

    parser.add_argument(
        "--show_tiles", dest="to_run", action="store_const", 
        const=show_tiles, default=None,
        help="Shows all available tiles in the game")

    parser.add_argument(
        "--show_map_layout", dest="to_run", action="store_const", 
        const=show_map_layout, default=None,
        help="Given a map shows the the tile id and unique id for every tile in the map. This can be used for knowing where to add triggers to the map")

    parser.add_argument(
        "--add_triggers", dest="to_run", action="store_const",
        const=add_triggers, default=None,
        help="Attach triggers from a json file to unique map tiles use the show_map_layout command to use when writing triggers."
    )

    parser.add_argument(
        "--show_triggers", dest="to_run", action="store_const",
        const=show_triggers, default=None,
        help="Shows all currently active triggers"
    )

    parser.add_argument("input_files", type=str, nargs="*",
                   help="input files")

    args = parser.parse_args()

    if not args.to_run:
        parser.error("No arguments provided")


    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "../../models/game.db")
    db = lite.connect(filename)
    db.row_factory = lite.Row
    with db:
        cursor = db.cursor()
        args.to_run(cursor, args.input_files)

def show_triggers(cursor, *args, **kwargs):
    cursor.execute("SELECT * FROM Trigger")
    rows = cursor.fetchall()
    for row in rows:
        print "MapTileId: %3d | Chance: %3d | Action_Type: %3d | Action_Data: %s" % (row['MapTileId'], row['Chance'], row['Action_Type'], str(json.loads(row['Action_Data'])))

def add_triggers(cursor, json_triggers_set, *args, **kwargs):
    for json_triggers in json_triggers_set:
        triggers_file = open(json_triggers)
        triggers = json.load(triggers_file)
        triggers_file.close()

        for trigger in triggers["triggers"]:
            cursor.execute(
                """INSERT INTO Trigger (MapTileId, Chance, Action_Type, Triggered_On,
                 Action_Data) VALUES (?, ?, ?, ?, ?)""",
                (trigger["MapTileId"], trigger["Chance"],
                 trigger["Action_Type"], trigger["Triggered_On"], json.dumps(trigger["Action_Data"])))

def show_map_layout(cursor, map_names, *args, **kwargs):
    show_tiles(cursor)
    cursor = cursor.execute(
            "SELECT * FROM Map WHERE Name='%s'" % map_names[0])
    loaded_map = cursor.fetchone()

    cursor.execute("SELECT * FROM MapTile WHERE MapId=%d" % loaded_map["Id"])

    map_tiles = cursor.fetchall()
    matrix = [[0 for x in xrange(Map.GRID_SIZE)] for x in xrange(Map.GRID_SIZE)] 
    for tile in map_tiles:
        matrix[tile["Index_Y"]][tile["Index_X"]] = tile

    print ""
    print "Showing layout for map: %s" % map_names[0]
    print ""
    print "Tile Identifier"
    print ""

    count = 0
    for column in range(Map.GRID_SIZE):
        for row in range(Map.GRID_SIZE):
            sys.stdout.write( "%5d" % (matrix[column][row]["TileId"]))
            count = count + 1
        print ""

    print ""
    print "Unique Tile Identifier"
    print ""

    count = 0
    for column in range(Map.GRID_SIZE):
        for row in range(Map.GRID_SIZE):
            sys.stdout.write( "%5d" % (matrix[column][row]["Id"]))
            count = count + 1
        print ""

    print ""
    print "Triggers"
    print ""

    show_triggers(cursor)

    print ""

def show_map_names(cursor, *args, **kwargs):
    result = cursor.execute(
                "SELECT * FROM Map")
    for row in result:
        print("Name: '%s', ID: '%s'" % (row[1], row[0]))


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

def create_maps(cursor, maps, *args, **kwargs):

    for a_map in maps:    
        reader = csv.reader(open(a_map, "rb"), delimiter=',')
        map_name = a_map
        if map_name.endswith(".csv"):
            map_name = map_name[:len(".csv")]
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


def update_map(cursor, map_arg, *args, **kwargs):
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


def delete_map_tiles(cursor, map_id,):
    cursor.execute(
        "DELETE FROM MapTile WHERE MapId = %s" % map_id)

def show_tiles(cursor, *args, **kwargs):
    cursor.execute("SELECT * FROM Tile")
    rows = cursor.fetchall()
    for row in rows:
        print "Id: %3d | Name: %s" % (row['Id'], row['Name'])


def add_tilesets(cursor, json_tilesets, *args, **kwargs):
    for json_tiles in json_tilesets:
        tiles_file = open(json_tiles)
        tiles = json.load(tiles_file)
        tiles_file.close()

        for tile in tiles["tiles"]:
            cursor.execute(
                "INSERT INTO Tile (Name, Image, Walkable) VALUES (?, ?, ?)",
                (tile["Name"], tile["Image"], tile["Walkable"]))


def reset_database(cursor, *args, **kwargs):
    # Clear DB of existing tables (focused on one map right now)
    cursor.execute("DROP TABLE IF EXISTS Map")
    cursor.execute("DROP TABLE IF EXISTS Tile")
    cursor.execute("DROP TABLE IF EXISTS MapTile")
    cursor.execute("DROP TABLE IF EXISTS Character")
    cursor.execute("DROP TABLE IF EXISTS Trigger")


    # Create tables (again if dropped before)
    cursor.execute(
        "CREATE TABLE Map"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT)")

    cursor.execute(
        "CREATE TABLE Tile"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Image TEXT, Walkable INTEGER)")

    cursor.execute(
        "CREATE TABLE MapTile"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, MapId INTEGER, TileId INTEGER, Index_X INTEGER, Index_Y INTEGER)")
   
    cursor.execute(
        "CREATE TABLE Character"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Image TEXT)")

    cursor.execute(
        "CREATE TABLE Trigger"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, MapTileId INTEGER, Chance INTEGER, Action_Type INTEGER, Triggered_On TEXT, Action_Data TEXT)")

    # Insert default data
    # Insert default character entry
    cursor.execute(
        "INSERT INTO Character (Image) VALUES (?)",
        ["ranger_m.png"])

    print("Database successfully reset to base data.")

if __name__ == "__main__":
    main()