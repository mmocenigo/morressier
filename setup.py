import sqlite3, csv, logging

db = sqlite3.connect('data/db.sql')
cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS location_info(id INTEGER PRIMARY KEY,
                                        type TEXT, duration REAL)
''')
db.commit()

cursor.execute("SELECT * FROM location_info")
row_count = len(cursor.fetchall())

if row_count is 0:
    try:
        with open('data/loc_types.csv', 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                cursor.execute('''
                INSERT INTO location_info (type, duration) 
                VALUES (?, ?);''', (row['type'], row['duration']))
                db.commit()
    except Exception as e:
        logging.exception("There was an issue importing the DB info.")

db.close()