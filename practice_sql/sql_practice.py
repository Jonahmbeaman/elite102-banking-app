import sqlite3

conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor() 

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        level INTEGER,
        is_legendary BOOLEAN
    )
''')

cursor.execute('''
    INSERT INTO pokemon (id, name, type, level, is_legendary)
    VALUES (1, 'Pickachu', 'Electric', 25, 0)
''')

cursor.execute('''
    INSERT INTO pokemon (id, name, type, level, is_legendary)
    VALUES (2, 'Charmander', 'Fire', 18, 0)
''')

cursor.execute('''
    INSERT INTO pokemon (id, name, type, level, is_legendary)
    VALUES (3, 'Mewtwo', 'Psychic', 70, 1)
''')

cursor.execute('''
    INSERT INTO pokemon (id, name, type, level, is_legendary)
    VALUES (4, 'Groudon', 'Ground/Fire', 100, 1)
''')



conn.commit()
conn.close()

print("pokemon inserted")