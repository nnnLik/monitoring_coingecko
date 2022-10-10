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
    print('----------------------------------------')
    print('1. The user table was successfully created')
    base.execute('''
                    CREATE TABLE IF NOT EXISTS wallet (
                        user_id TEXT,
                        coin_id TEXT,
                        value_of_coins REAL DEFAULT 0.0, 
                        FOREIGN KEY (user_id) REFERENCES user(user_id))
                ''')
    print('----------------------------------------')
    print('2. The coins wallet was successfully created')
    print('----------------------------------------')
    base.execute('''
                    CREATE TABLE IF NOT EXISTS list_of_coin (
                        coin_id TEXT PRIMARY KEY UNIQUE,
                        coin_name TEXT,
                        get_method TEXT)
                ''')

    print('3. The list_of_coins wallet was successfully created')
    print('----------------------------------------')
    print('Filling the database with a list of coins')

    try:
        cur.execute('''INSERT INTO list_of_coin (coin_id, coin_name, get_method)
                            VALUES 
                                ('bitcoin', 'BTC - Bitcoin', 'https://api.coingecko.com/api/v3/coins/bitcoin'),
                                ('ethereum', 'ETH - Ethereum', 'https://api.coingecko.com/api/v3/coins/eth'),
                                ('true-usd', 'TUSD - TrueUSD', 'https://api.coingecko.com/api/v3/coins/true-usd'),
                                ('tether', 'USDT - Tether', 'https://api.coingecko.com/api/v3/coins/tether'),
                                ('binancecoin', 'BNB - Bnb', 'https://api.coingecko.com/api/v3/coins/binancecoin'),
                                ('ripple', 'XRP - Ripple', 'https://api.coingecko.com/api/v3/coins/ripple'),
                                ('cardano', 'ADA - Cardano', 'https://api.coingecko.com/api/v3/coins/cardano'),
                                ('dogecoin', 'Doge - Dogecoin', 'https://api.coingecko.com/api/v3/coins/dogecoin'),
                                ('solana', 'SOL - Solana', 'https://api.coingecko.com/api/v3/coins/solana'),
                                ('polkadot', 'DOT - Polkadot', 'https://api.coingecko.com/api/v3/coins/polkadot'),
                                ('shiba-inu', 'SHIB - Shiba Inu', 'https://api.coingecko.com/api/v3/coins/shiba-inu'),
                                ('dai', 'DAI - Dai', 'https://api.coingecko.com/api/v3/coins/dai'),
                                ('matic-network', 'MATIC - Polygon', 'https://api.coingecko.com/api/v3/coins/matic-network'),
                                ('tron', 'TRX - TRON', 'https://api.coingecko.com/api/v3/coins/tron'),
                                ('uniswap', 'UNI - Uniswap', 'https://api.coingecko.com/api/v3/coins/uniswap'),
                                ('wrapped-bitcoin', 'WBTC - Wrapped Bitcoin', 'https://api.coingecko.com/api/v3/coins/wrapped-bitcoin'),
                                ('chainlink', 'LINK - Chainlink', 'https://api.coingecko.com/api/v3/coins/chainlink'),
                                ('leo-token', 'LEO - LEO Token', 'https://api.coingecko.com/api/v3/coins/leo-token'),
                                ('cosmos', 'ATOM - Cosmos Hub', 'https://api.coingecko.com/api/v3/coins/cosmos'),
                                ('litecoin', 'LTC - Litecoin', 'https://api.coingecko.com/api/v3/coins/litecoin')
                        ''')
    except:
        print('Fail')
    else:
        print('Success')
    base.commit()


async def check_user(user_id):
    info = cur.execute('SELECT user_id FROM user WHERE user_id=?', (user_id,))

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


async def set_user_wallet(user_id, coin_id, value_of_coins):
    cur.execute('''INSERT INTO wallet VALUES (
                                            user_id,
                                            wallet_id,
                                            balance,
                                            wallet_currency)''', (
        user_id,
        coin_id,
        value_of_coins)
                )

    base.commit()
