import logging

from aiogram import (
    Bot,
    Dispatcher,
)

from config import settings

logging.basicConfig(level=logging.INFO)

basic_message = "Choose the functionality you are interested in"

bot = Bot(token=settings["TOKEN"])
dp = Dispatcher(bot=bot)
