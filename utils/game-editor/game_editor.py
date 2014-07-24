import sqlite3 as lite
import csv
import sys
import os
import json
import argparse

from Unrealistic_Engine.models.map import Map


def main():
    parser = argparse.ArgumentParser(
        description="Utility to create games in Unrealistic Engine"
    )

    parser.add_argument(
        "--reset", dest="to_run", action="store_const", 
        const=reset_database, default=None,
        help="Resets the game database to default state"
    )

    parser.add_argument(
        "--show_map_names", dest="to_run", action="store_const", 
        const=show_map_names, default=None,
        help="Displays the names of all loaded maps"
    )

    parser.add_argument(
        "--add_maps", dest="to_run", action="store_const",
        const=add_maps, default=None,
        help="Creates a map using a passed in .json file"
    )

    parser.add_argument(
        "--add_tileset", dest="to_run", action="store_const", 
        const=add_tilesets, default=None,
        help="Adds a .json defined tileset to the game"
    )

    parser.add_argument(
        "--show_tiles", dest="to_run", action="store_const", 
        const=show_tiles, default=None,
        help="Shows all available tiles in the game"
    )

    parser.add_argument(
        "--show_map_layout", dest="to_run", action="store_const", 
        const=show_map_layout, default=None,
        help="Given a map shows the the tile id and unique id for every tile in the map. \
              This can be used for knowing where to add triggers to the map"
    )

    parser.add_argument(
        "--add_triggers", dest="to_run", action="store_const",
        const=add_triggers, default=None,
        help="Attach triggers from a json file to unique map tiles use the show_map_layout command \
              to use when writing triggers."
    )

    parser.add_argument(
        "--show_triggers", dest="to_run", action="store_const",
        const=show_triggers, default=None,
        help="Shows all currently active triggers"
    )

    parser.add_argument(
        "--add_enemies", dest="to_run", action="store_const",
        const=add_enemies, default=None,
        help="Adds a .json file defined enemy list to the game"
    )

    parser.add_argument(
        "--add_items", dest="to_run", action="store_const",
        const=add_items, default=None,
        help="Adds a .json file defined item list to the game"
    )

    parser.add_argument(
        "--create_game", dest="to_run", action="store_const",
        const=create_game, default=None,
        help="Builds a complete game using the files specified in the given file. Runs, in order, \
              --reset, --add_tileset, --create_map, --add_triggers, and --add_enemies"
    )

    parser.add_argument(
        "input_files",
        type=str, nargs="*",
        help="input files"
    )

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
        print "MapTileId: %3d | Chance: %3d | Action_Type: %s | Action_Data: %s" % (row['MapTileId'],
                row['Chance'], str(row['Action_Type']), str(json.loads(row['Action_Data'])))


def add_triggers(cursor, json_triggers_set, *args, **kwargs):
    for json_triggers in json_triggers_set:
        triggers_file = open(json_triggers)
        triggers = json.load(triggers_file)
        triggers_file.close()

        for trigger in triggers["triggers"]:
            cursor.execute(
                """INSERT INTO Trigger (MapTileId, Chance, Action_Type,
                Triggered_On, Direction_Facing, One_Time,
                 Action_Data) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (trigger["MapTileId"], trigger["Chance"],
                 trigger["Action_Type"], trigger["Triggered_On"],
                 trigger["Direction_Facing"], trigger["One_Time"],
                 json.dumps(trigger["Action_Data"])))
    print("Triggers added successfully.")


def create_game(cursor, game_index_file, *args, **kwargs):
    index_file = open(game_index_file[0])
    game_index = json.load(index_file)
    index_file.close()
    
    reset_database(cursor)
    
    add_tilesets (cursor, game_index["tilesets"])
    add_maps (cursor, game_index["maps"])
    add_triggers (cursor, game_index["triggers"])
    add_enemies (cursor, game_index["enemies"])
    add_items(cursor, game_index["items"])


def show_map_layout(cursor, map_names, *args, **kwargs):
    show_tiles(cursor)
    cursor = cursor.execute(
            "SELECT * FROM Map WHERE Name='%s'" % map_names[0])
    loaded_map = cursor.fetchone()

    cursor = cursor.execute(
            "SELECT * FROM MapLayer WHERE MapId='%d'" % loaded_map["Id"])
    loaded_layers = cursor.fetchall()

    for layer in loaded_layers:
        cursor.execute("SELECT * FROM MapTile WHERE MapLayerId=%d" % layer["Id"])

        map_tiles = cursor.fetchall()
        matrix = [[0 for x in xrange(Map.GRID_SIZE)] for x in xrange(Map.GRID_SIZE)]
        for tile in map_tiles:
            matrix[tile["Index_Y"]][tile["Index_X"]] = tile

        print ""
        print "Showing layout for map: %s" % map_names[0]
        print "Layer: %s" % layer["Layer"]
        print "Tile Identifier"
        print ""

        count = 0
        for column in range(Map.GRID_SIZE):
            for row in range(Map.GRID_SIZE):
                sys.stdout.write( "%5d" % (matrix[column][row]["TileId"]))
                count += 1
            print ""

        print ""
        print "Unique Tile Identifier"
        print ""

        count = 0
        for column in range(Map.GRID_SIZE):
            for row in range(Map.GRID_SIZE):
                sys.stdout.write( "%5d" % (matrix[column][row]["Id"]))
                count += 1
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


def insert_map(cursor, map_name, music):
    cursor.execute(
        "INSERT INTO Map (Name, Music) VALUES (?, ?)",
        [map_name, music])


def insert_map_layer(cursor, layer, map_id):
    cursor.execute(
        "INSERT INTO MapLayer (Layer, MapId) VALUES (?, ?)",
            [layer, map_id])


def get_map_id(cursor, map_name):
    result = cursor.execute(
                "SELECT ID FROM Map WHERE NAME = '%s'"
                % map_name)
    for row in result:
        return row[0]

def get_map_layer_id(cursor, map_id, layer):
    result = cursor.execute(
                "SELECT ID FROM MapLayer WHERE MapId = '%d' AND Layer= '%s'"
                % (map_id, layer))
    for row in result:
        return row[0]


def insert_maptile(cursor, map_layer_id, tile_id, x_pos, y_pos):
    cursor.execute(
        "INSERT INTO MapTile (MapLayerId, TileId, Index_X, Index_Y) VALUES (?, ?, ?, ?)",
        (map_layer_id, tile_id, x_pos, y_pos))


def add_maps(cursor, maps, *args, **kwargs):
    for a_map in maps:
        map_file = open(a_map)
        the_map = json.load(map_file)
        map_file.close()

        map_name = a_map
        if map_name.endswith(".json"):
            map_name = map_name[:(len(map_name) - len(".json"))]

        insert_map(cursor, map_name, the_map["Music"])
        map_id = get_map_id(cursor, map_name)

        layer = "Layer1"
        insert_map_layer(cursor, layer, map_id)
        map_layer_id = get_map_layer_id(cursor, map_id, layer)
        cur_row = 0
        for row in the_map[layer]:
            entries = row.split(',')
            cur_col = 0
            for entry in entries:
                insert_maptile(cursor, map_layer_id, entry, cur_col, cur_row)
                cur_col += 1
            cur_row += 1

        layer = "Layer2"
        insert_map_layer(cursor, layer, map_id)
        map_layer_id = get_map_layer_id(cursor, map_id, layer)
        cur_row = 0
        for row in the_map[layer]:
            entries = row.split(',')
            cur_col = 0
            for entry in entries:
                insert_maptile(cursor, map_layer_id, entry, cur_col, cur_row)
                cur_col += 1
            cur_row += 1

        print("Map with name '%s' was successfully created." % map_name)  


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
    print("Tilesets added successfully.")


def add_enemies(cursor, json_enemies_set, *args, **kwargs):
    for json_enemies in json_enemies_set:
        enemies_file = open(json_enemies)
        enemies = json.load(enemies_file)
        enemies_file.close()

        for enemy in enemies["enemies"]:
            cursor.execute(
                """INSERT INTO Character (Name, Image, Health, Attack, Defense) VALUES (?, ?, ?, ?, ?)""",
                (enemy["Name"], enemy["Image"], enemy["Health"], enemy["Attack"], enemy['Defense']))
    print("Enemies added successfully.")


def add_items(cursor, json_items_set, *args, **kwargs):
    for json_items in json_items_set:
        items_file = open(json_items)
        items = json.load(items_file)
        items_file.close()

        for item in items["items"]:
            cursor.execute(
                """INSERT INTO Item (Name, Type, Modifier, Slot, Description) VALUES (?, ?, ?, ?, ?)""",
                (item["Name"], item["Type"], item["Modifier"], item['Slot'], item["Description"]))
    print("Items added successfully")


def reset_database(cursor, *args, **kwargs):
    # Clear DB of existing tables
    cursor.execute("DROP TABLE IF EXISTS Map")
    cursor.execute("DROP TABLE IF EXISTS MapLayer")
    cursor.execute("DROP TABLE IF EXISTS Tile")
    cursor.execute("DROP TABLE IF EXISTS MapTile")
    cursor.execute("DROP TABLE IF EXISTS Character")
    cursor.execute("DROP TABLE IF EXISTS Trigger")
    cursor.execute("DROP TABLE IF EXISTS GameState")
    cursor.execute("DROP TABLE IF EXISTS Item")
    cursor.execute("DROP TABLE IF EXISTS InventoryState")

    # Create tables (again if dropped before)
    cursor.execute(
        "CREATE TABLE Map"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Music TEXT)")

    cursor.execute(
        "CREATE TABLE MapLayer"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Layer TEXT, MapId INTEGER)")

    cursor.execute(
        "CREATE TABLE Tile"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Image TEXT, Walkable INTEGER)")

    cursor.execute(
        "CREATE TABLE MapTile"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, MapLayerId INTEGER, TileId INTEGER, Index_X INTEGER, "
        "Index_Y INTEGER)")
   
    cursor.execute(
        "CREATE TABLE Character"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Image TEXT, Health INTEGER, "
        "Attack INTEGER, Defense INTEGER)")

    cursor.execute(
        "CREATE TABLE Trigger"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, MapTileId INTEGER, Chance INTEGER, "
        "Action_Type INTEGER, Triggered_On TEXT, Direction_Facing TEXT, "
        "One_Time INTEGER,  Action_Data TEXT)")

    cursor.execute(
        "CREATE TABLE GameState"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Current_Map TEXT, Character_Position_X INTEGER, "
        "Character_Position_Y INTEGER, Character_Health INTEGER, Character_Total_Health INTEGER,"
        "Character_Attack INTEGER, Character_Defense INTEGER)")

    cursor.execute(
        "CREATE TABLE Item"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Type INTEGER, Slot INTEGER, Modifier INTEGER, "
        "Description TEXT)"
    )

    cursor.execute(
        "CREATE TABLE InventoryState"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Game_State_ID INTEGER, Item_ID INTEGER, Equipped INTEGER, Quantity INTEGER)"
    )

    # Insert default data
    # Insert default character entry
    cursor.execute(
        "INSERT INTO Character (Name, Image, Health, Attack, Defense) VALUES (?, ?, ?, ?, ?)",
        ("Player", "warrior", 200, 50, 10))

    print("Database successfully reset to base data.")

if __name__ == "__main__":
    main()
