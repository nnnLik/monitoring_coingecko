import requests

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import settings
from coins_configs import ALL_COINS, LIST_OF_COINS

from sсhemas import MarketDataModel

from data_base import sqlite_db


logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings['TOKEN'])
dp = Dispatcher(bot=bot)

basic_message = 'Choose the functionality you are interested in'


class SelectCurrencyCP(StatesGroup):
    select_currency = State()


# inline keyboard buttons

# "Change tracked coins" buttons
inline_keyboard_ctc = InlineKeyboardMarkup(row_width=2)
inline_keyboard_ctc_buttons = [InlineKeyboardButton(text='🟢 ADD', callback_data='ctc_add'),
                               InlineKeyboardButton(text='🔴 DELETE', callback_data='ctc_delete')]
inline_keyboard_ctc.row(*inline_keyboard_ctc_buttons)

# "Check price" buttons
inline_keyboard_cp = InlineKeyboardMarkup(row_width=2)
inline_keyboard_cp_buttons = [InlineKeyboardButton(text='＄ - USD', callback_data='cp_usd'),
                              InlineKeyboardButton(text='€ - EUR', callback_data='cp_eur'),
                              InlineKeyboardButton(text='₽ - RUB', callback_data='cp_rub')]
inline_keyboard_cp.row(*inline_keyboard_cp_buttons)


@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message) -> None:
    buttons = [

        "📊 Monitoring",
        "🏦 Wallet",

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message,
                         reply_markup=keyboard)


# @dp.message_handler(lambda message: message.text == "🏦 Wallet")
# async def monitoring(message: types.Message):
#
#     buttons = [
#
#         "View monitored currencies",
#         "Show exchange rate",
#         "Back"
#
#     ]
#
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*buttons)
#
#     await message.answer(basic_message,
#                          reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "📊 Monitoring")
async def monitoring(message: types.Message):
    buttons = [

        "📈 Check price",
        "✍🏻 Tracked coins",
        "📜 List of coins",
        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message,
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "✍🏻 Tracked coins")
async def currencies(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(
        '👋 Here you see information about the currently tracked coins, the price of which you can see in the *📈 Check price* tab.',
        parse_mode="Markdown")

    for coin in ALL_COINS:
        ch_coin = ALL_COINS[coin][0]
        await message.answer(ch_coin,
                             reply_markup=keyboard)

    await message.answer(
        'You can add a coin you are interested in by clicking *🟢 ADD*, or you can remove it by clicking *🔴 DELETE*.',
        parse_mode="Markdown",
        reply_markup=inline_keyboard_ctc)


@dp.message_handler(lambda message: message.text == "📈 Check price")
async def currencies(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer('Select the currency to which you want to see the coin price',
                         reply_markup=inline_keyboard_cp)


@dp.message_handler(lambda message: message.text == "📜 List of coins")
async def currencies(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    for coins in LIST_OF_COINS:
        name_of_coin = ''
        await message.answer(f'Coin Name: *{LIST_OF_COINS[coins]["name"]}*\nCoin ID: _{LIST_OF_COINS[coins]["id"]}_',
                             parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == "🔙 Back")
async def back(message: types.Message):
    buttons = [

        "📊 Monitoring",
        "🏦 Wallet",

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message,
                         reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('ctc_'))
async def ctc_add(callback: types.CallbackQuery):
    ctc_answer = str(callback.data.split('_')[1])
    if ctc_answer == 'add':
        pass
    if ctc_answer == 'delete':
        pass


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cp_'))
async def ctc_add(callback: types.CallbackQuery):
    cp_answer = str(callback.data.split('_')[1]).upper()

    test_str_price = ''

    for coin in ALL_COINS:
        ch_coin = ALL_COINS[coin][1]
        response = requests.get(ch_coin).json()

        coin_price = str(MarketDataModel(**response))

        pars_price = coin_price.split('CurrentPrice')[1].replace(" ", "").replace(")", "").replace("(", "")
        list_of_prices = pars_price.split(',')

        if cp_answer == 'USD':
            price = list_of_prices[0][4:]
            test_str_price += f'*{ALL_COINS[coin][0]}* --> {price} ＄\n'
        elif cp_answer == 'EUR':
            price = list_of_prices[1][4:]
            test_str_price += f'*{ALL_COINS[coin][0]}* --> {price} €\n'
        elif cp_answer == 'RUB':
            price = list_of_prices[2][4:]
            test_str_price += f'*{ALL_COINS[coin][0]}* --> {price} ₽\n'

    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                parse_mode="Markdown",
                                text=test_str_price)


async def main():
    sqlite_db.sql_start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
