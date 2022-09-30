import sqlite3


def sql_start():
    global base, cur
    base = sqlite3.connect('wallet_db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS wallet(user_id INTEGER PRIMARY KEY, balance FLOAT)')
    base.commit()


async def check_user(user_id):
    info = cur.execute('SELECT user_id FROM wallet WHERE user_id=?', (user_id,))

    if info.fetchone() is None:
        cur.execute('INSERT INTO wallet VALUES (?, ?)', (user_id, 1000))
    else:
        raise ValueError


