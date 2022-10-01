import sqlite3

import random


class NoneUserWallet(Exception):
    pass


def sql_start():
    global base, cur
    base = sqlite3.connect('wallet_db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('''
                    CREATE TABLE IF NOT EXISTS wallet(
                    user_id INTEGER PRIMARY KEY,
                    wallet_id INTEGER,
                    balance NULL,
                    coins NULL,
                    value_of_user_coins NULL)
                ''')
    base.commit()


async def check_user(user_id):
    info = cur.execute('SELECT user_id FROM wallet WHERE user_id=?', (user_id,))

    if info.fetchone() is None:
        pass
    else:
        raise NoneUserWallet


# async def create_wallet(user_id):
#
#     while True:
#         wallet_address = random.randint(1, 1_000_000)
#         info = cur.execute('SELECT wallet_id FROM wallet WHERE wallet_id=?', (wallet_address,))
#         if info.fetchone() is None:
#             pass
#         else:
#             cur.execute('INSERT INTO wallet VALUES (?, ?, ?)', (user_id, wallet_address, 1000))
#             raise CreateWallet
#
#
# async def view_inf():
#     output_check_inf = str(cur.execute(f'SELECT wallet_id FROM wallet WHERE wallet_id = 1').fetchone()[0])
#     print(output_check_inf)
#

