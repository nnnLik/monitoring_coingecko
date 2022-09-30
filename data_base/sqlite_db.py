import sqlite3


def sql_start():
    global base, cur
    base = sqlite3.connect('wallet_db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS wallet(user_id INTEGER PRIMARY KEY, balance FLOAT)')
    base.commit()