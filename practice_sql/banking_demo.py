import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE contacts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')

contacts_to_add = [
    (1, 'Matt Beaman', 'matt@griddle.biz'),
    (2, 'Jonah Beaman', 'jonah@uccs.edu'),
]

cursor.executemany(
    "INSERT INTO contacts VALUES (?, ?, ?)",
    contacts_to_add
)


third_contact = (3, 'John Doe', '123@gmail.com')
cursor.execute(
    "INSERT INTO contacts VALUES (?, ?, ?)",
    third_contact
)

conn.commit()


print("\n=== EMAILS AT @griddle.biz ===")
cursor.execute(
    "SELECT * FROM contacts WHERE email LIKE ?",
    ('%@griddle.biz',)
)
for row in cursor.fetchall():
    print(row)
conn.commit()

print("=== ALL CONTACTS ===")
cursor.execute("SELECT * FROM contacts")
for row in cursor.fetchall():
    print(row)

search_name = "Jonah Beaman"
cursor.execute("SELECT * FROM contacts WHERE name = ?", (search_name,))
result = cursor.fetchone()
print(f"\n=== LOOKUP FOR '{search_name}' ===")
print(result)

conn.close()