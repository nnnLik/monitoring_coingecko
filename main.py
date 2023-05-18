import asyncio

import logging

from data_base import sqlite_db

from imports import (
    dp,
    bot,
)

from handlers import start
from handlers.wallet_handlers import wallet
from handlers.monitoring_handlers import monitoring

logging.basicConfig(level=logging.INFO)

start.register_start_handlers(dp)
wallet.register_wallet_handlers(dp)
monitoring.register_monitoring_handlers(dp)


async def main():
    sqlite_db.sql_start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
