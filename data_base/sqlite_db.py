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
                    CREATE TABLE IF NOT EXISTS coins (
                        user_id TEXT,
                        coin TEXT,
                        value REAL
                    )
                ''')
    print('The coins table was successfully created')
    base.execute('''
                    CREATE TABLE IF NOT EXISTS wallet (
                                                        user_id TEXT PRIMARY KEY,
                                                        wallet_id TEXT,
                                                       balance FLOAT,
                                                        wallet_currency TEXT,
                                                        coins TEXT,
                                                        FOREIGN KEY (user_id) REFERENCES coins(user_id)
                    )
                ''')
    print('The wallet table was successfully created')
    base.commit()


async def check_user(user_id):
    info = cur.execute('SELECT user_id FROM wallet WHERE user_id=?', (user_id,))

    if info.fetchone() is None:
        pass
    else:
        raise NoneUserWallet


async def create_wallet(user_id, wallet_currency):

    wallet_address = str(user_id) + '_wallet'
    cur.execute('''INSERT INTO wallet VALUES (
                                            user_id,
                                            wallet_id,
                                            balance,
                                            wallet_currency)''', (
                                                                user_id,
                                                                wallet_address,
                                                                0,
                                                                wallet_currency)
                )

    base.commit()
    return wallet_address
