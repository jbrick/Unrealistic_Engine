import sqlite3 as lite

db = lite.connect('game.db')
with db:
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Maps")
    cursor.execute("DROP TABLE IF EXISTS Tiles")
    cursor.execute("DROP TABLE IF EXISTS MapTile")
    cursor.execute("DROP TABLE IF EXISTS Character")

    cursor.execute(
        "CREATE TABLE Maps"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT)")
    
    cursor.execute(
        "CREATE TABLE Tiles"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Image TEXT)")

    cursor.execute(
        "CREATE TABLE MapTile"
        "(MapId INTEGER, TileId INTEGER, Index_X INTEGER, Index_Y INTEGER)")
   
    cursor.execute(
        "CREATE TABLE Character"
        "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Image TEXT)")

    cursor.execute(
        "INSERT INTO Character (Image) VALUES (?)",
        ["Images/ball.bmp"])

    cursor.execute(
        "INSERT INTO Maps (Name) VALUES (?)",
        ["Basic"])

    cursor.execute(
        "INSERT INTO Tiles (Image) VALUES (?)",
        ["Images/tile1.bmp"])

    cursor.execute(
        "INSERT INTO MapTile VALUES (?, ?, ?, ?)",
        (1, 1, 1, 1))

    cursor.execute(
        "INSERT INTO MapTile VALUES (?, ?, ?, ?)",
        (1, 1, 2, 1))
