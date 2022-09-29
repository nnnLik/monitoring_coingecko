import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('wallet_db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    # base.execute('CREATE TABLE IF NOT EXISTS ')