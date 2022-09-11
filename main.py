import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, types
from config import settings

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings['TOKEN'])

dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message):
    buttons = [

        "Monitoring",
        "Buy",

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer('Choose the functionality you are interested in', reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Monitoring")
async def monitoring(message: types.Message):
    buttons = [

        "View monitored currencies",
        "Show exchange rate",
        "Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(' ',
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "View monitored currencies")
async def currencies(message: types.Message):
    buttons = [
        "Back"
    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    monitored_currencies = requests.get(f'https://api.coingecko.com/api/v3//coins/list').json()

    await message.answer(' ',
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Back")
async def back(message: types.Message):
    buttons = [

        "Monitoring",
        "Buy",

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer('Choose the functionality you are interested in', reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
