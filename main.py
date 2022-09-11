import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, types

from config import settings
from coins import all_coins

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings['TOKEN'])

dp = Dispatcher(bot=bot)

basic_message = 'Choose the functionality you are interested in'


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

    await message.answer(basic_message,
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "View monitored currencies")
async def currencies(message: types.Message):

    buttons = [

        "Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    for coin in all_coins:
        ch_coin = all_coins[coin][0]
        await message.answer(ch_coin, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Show exchange rate")
async def currencies(message: types.Message):

    buttons = [

        "Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    for coin in all_coins:
        ch_coin = all_coins[coin][1]
        response = requests.get(ch_coin).json()
        await message.answer(ch_coin, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Back")
async def back(message: types.Message):

    buttons = [

        "Monitoring",
        "Buy",

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message, reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
