import sqlite3, logging

db = sqlite3.connect('data/db.sql')

def get_location_type(max_hours):
    try:
        cursor = db.cursor()
        cursor.execute('''
        SELECT location_info.type, location_info.duration FROM location_info
        WHERE location_info.duration <= ?
        ORDER BY RANDOM()
        LIMIT 1;
        ''', (max_hours,))
        return cursor.fetchone()
    except Exception as e:
        logging.exception("Could not retrieve location info from DB")

