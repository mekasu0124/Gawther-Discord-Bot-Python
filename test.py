import sqlite3 as sql 

with sql.connect('main.db') as mdb:
    cur = mdb.cursor()

    all_ids = cur.execute('SELECT id FROM members').fetchall()

    print(all_ids)

    for id in all_ids:
        print(id[0])