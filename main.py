import requests

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging

from config import settings
from coins import all_coins

from sсhemas import Model

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings['TOKEN'])

dp = Dispatcher(bot=bot)

basic_message = 'Choose the functionality you are interested in'

DELAY = 5

chat_id = 475835202


async def update_price():
    await dp.bot.send_message(chat_id, '\nTimer message')


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


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
        "Change notification time",
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

        coin_price = str(Model(**response))

        pars_price = coin_price.split('CurrentPrice')[1].replace(" ", "").replace(")", "").replace("(", "")
        list_of_prices = pars_price.split(',')

        usd_price = list_of_prices[0][4:]
        eur_price = list_of_prices[1][4:]
        rub_price = list_of_prices[2][4:]

        coin_price = f'''
        
{all_coins[coin][0]} / USD --> {usd_price}
{all_coins[coin][0]} / EUR --> {eur_price}
{all_coins[coin][0]} / RUB --> {rub_price}
        
                    '''

        await message.answer(coin_price, reply_markup=keyboard)


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
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, update_price, loop)
    executor.start_polling(dp, loop=loop)
    asyncio.run(main())
