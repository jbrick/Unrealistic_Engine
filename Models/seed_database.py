import sqlite3 as lite

db = lite.connect('game.db')
with db:
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Character")

    query = ( "CREATE TABLE Character"
              "(Id INTEGER PRIMARY KEY AUTOINCREMENT, Image TEXT)")
    cursor.execute(query)
    with open ("../Images/character.bmp") as f:
        blob = f.read()

    cursor.execute(
        "INSERT INTO Character (Image) VALUES (?)",
        ["../Images/character.bmp"])
