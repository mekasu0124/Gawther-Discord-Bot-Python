import sqlite3 as sql


def create_db():
    with sql.connect('main.db') as mdb:
        cur = mdb.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS members(
            id INTEGER,
            exp INTEGER,
            level INTEGER,
            color TEXT,
            animal TEXT,
            food TEXT,
            edu_subj TEXT,
            artist_music TEXT,
            artist_art TEXT,
            season TEXT,
            holiday TEXT,
            warnings INTEGER,
            mutes INTEGER,
            bans INTEGER,
            kicks INTEGER,
            age INTEGER,
            dob TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS ban_logs(
            id INTEGER,
            ban_id INTEGER,
            staff TEXT,
            start_time TEXT,
            end_time TEXT,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS mute_logs(
            id INTEGER,
            mute_id INTEGER,
            staff TEXT,
            start_time TEXT,
            end_time TEXT,
            reason TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS kick_logs(
            id INTEGER,
            kick_id INTEGER,
            staff TEXT,
            start_time TEXT,
            end_time TEXT,
            reason TEXT
        )''')