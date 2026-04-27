import sqlite3

conn = sqlite3.connect('pokemon.db')
cursor = conn.cursor()

print("=== ALL POKEMON ===")
cursor.execute("SELECT * FROM pokemon")
for row in cursor.fetchall():
    print(row)


print("\n=== NAMES AND TYPES ONLY ===")
cursor.execute("SELECT name, type FROM pokemon")
for row in cursor.fetchall():
    print(row)


print("\n=== FIRE TYPES ===")
cursor.execute("SELECT * FROM pokemon WHERE type = 'Fire'")
for row in cursor.fetchall():
    print(row)


print("\n=== LEVEL > 20 AND NOT ELECTRIC ===")
cursor.execute("SELECT * FROM pokemon WHERE level > 20 AND type != 'Electric'")
for row in cursor.fetchall():
    print(row)

print("\n=== LEVEL > 50 AND IS LEGENDARY ===")
cursor.execute("SELECT * FROM pokemon WHERE level > 50 AND is_legendary = 1")
for row in cursor.fetchall():
    print(row)

conn.close()