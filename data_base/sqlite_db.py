import sqlite3


class NoneUserWallet(Exception):
    pass


def sql_start():
    global base, cur
    base = sqlite3.connect('global_db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    else:
        print('Data base was created!')

    base.execute('''
                    CREATE TABLE IF NOT EXISTS user (
                        user_id TEXT PRIMARY KEY UNIQUE NOT NULL,
                        wallet_id TEXT NOT NULL,
                        balance REAL DEFAULT 0.0)
                ''')
    print('''----------------------------------------\n
    The user table was successfully created\n''')
    base.execute('''
                    CREATE TABLE IF NOT EXISTS list_of_coin (
                        coin_id TEXT PRIMARY KEY UNIQUE NOT NULL,
                        coin_name TEXT,
                        get_method TEXT)
                ''')
    print('''----------------------------------------\n
    The list_of_coin table was successfully created\n
    ----------------------------------------''')
    base.execute('''
                    CREATE TABLE IF NOT EXISTS wallet (
                        user_id TEXT,
                        coin_id TEXT,
                        value_of_coins REAL DEFAULT 0.0, 
                        FOREIGN KEY (user_id) REFERENCES user(user_id)
                ''')
    print('''----------------------------------------\n
    The coins wallet was successfully created\n
    ----------------------------------------''')

    base.commit()
