import sqlite3


class NoneUserWallet(Exception):
    pass


def sql_start():
    global base, cur
    base = sqlite3.connect('global_db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('''
                    CREATE TABLE IF NOT EXISTS wallet(
                    user_id INTEGER PRIMERY KEY,
                    wallet_id TEXT
                    )
                ''')
    print('Data base was created!')
    base.commit()


async def check_user(user_id):
    info = cur.execute('SELECT user_id FROM wallet WHERE user_id=?', (user_id,))

    if info.fetchone() is None:
        pass
    else:
        raise NoneUserWallet


async def create_wallet(user_id):

    wallet_address = str(user_id) + '_wallet'
    cur.execute("INSERT INTO wallet VALUES (?, ?)", (user_id, wallet_address))
    base.commit()

    return wallet_address


# async def view_inf():
#     output_check_inf = str(cur.execute(f'SELECT wallet_id FROM wallet WHERE wallet_id = 1').fetchone()[0])
#     print(output_check_inf)
#

