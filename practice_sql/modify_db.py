import sqlite3

conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()


cursor.execute('''
    UPDATE pokemon
    SET name = 'Pikachu'
    WHERE id = 1
''')

cursor.execute('''
    UPDATE pokemon
    SET level = 25
    WHERE name = 'Charmander'
''')

cursor.execute('''
    DELETE FROM pokemon
    WHERE id = 3
''')

cursor.execute('''
    UPDATE pokemon
    SET level = level + 5
    WHERE name = 'Groudon'
''')

cursor.execute('''
    DELETE FROM pokemon
    WHERE level < 30
''')

conn.commit()
conn.close()

print("Database modified!")