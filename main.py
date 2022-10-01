import requests

import asyncio

from aiogram import (Bot, Dispatcher, types, )
import logging

from aiogram.dispatcher.filters.state import (State, StatesGroup, )

from keyboards.inline_change_coins import inline_keyboard_CTC
from keyboards.inline_check_price import inline_keyboard_CP
from keyboards.inline_create_wallet import inline_keyboard_CW

from data_base import sqlite_db
from data_base.sqlite_db import NoneUserWallet

from config import settings
from coins_configs import (ALL_COINS, LIST_OF_COINS, )

from schemas.schemas_list_of_coins import ListOfCoinsModel
from schemas.sсhemas_current_price import MarketDataModel

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings['TOKEN'])
dp = Dispatcher(bot=bot)

basic_message = 'Choose the functionality you are interested in'


class SelectCurrencyCP(StatesGroup):
    select_currency = State()


@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message) -> None:
    buttons = [

        "📊 Monitoring",
        "🏛 Wallet",

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message,
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "🏛 Wallet")
async def monitoring(message: types.Message):

    user_id = message.from_user.id

    try:
        await sqlite_db.check_user(user_id)

    except NoneUserWallet:
        buttons = [

            "💳 Check the balance",
            "🛍 Buy / Sell",
            "🔙 Back"

        ]

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*buttons)

        await message.answer(basic_message,
                             reply_markup=keyboard)

    else:
        buttons = [

            "🔙 Back"

        ]

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*buttons)

        await message.answer("Let's start", reply_markup=keyboard)

        await message.answer(
            'To start work you need to __*create wallet*__',
            parse_mode="Markdown",
            reply_markup=inline_keyboard_CW)


@dp.message_handler(lambda message: message.text == "💳 Check the balance")
async def monitoring(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message,
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "🛍 Buy / Sell")
async def monitoring(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message,
                         reply_markup=keyboard)


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
        reply_markup=inline_keyboard_CTC)


@dp.message_handler(lambda message: message.text == "📈 Check price")
async def currencies(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer('Select the currency to which you want to see the coin price',
                         reply_markup=inline_keyboard_CP)


@dp.message_handler(lambda message: message.text == "📜 List of coins")
async def currencies(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    for coins in LIST_OF_COINS:
        await message.answer(f'Coin Name: *{LIST_OF_COINS[coins]["name"]}*\nCoin ID: _{LIST_OF_COINS[coins]["id"]}_',
                             parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == "🔙 Back")
async def back(message: types.Message):
    buttons = [

        "📊 Monitoring",
        "🏛 Wallet",

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message,
                         reply_markup=keyboard)


@dp.callback_query_handler(lambda command: command.data and command.data.startswith('CREATE'))
async def create_wallet(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name
    wallet_address = await sqlite_db.create_wallet(user_id)
    await bot.edit_message_text(
        text=f'''
        A wallet was created for the <b>{first_name}</b> and the address of this wallet <u>{wallet_address}</u>.\n
🥳Congrats!🥳
             ''',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        parse_mode='html')


@dp.callback_query_handler(lambda command: command.data and command.data.startswith('CTC_'))
async def ctc_add(callback: types.CallbackQuery):
    ctc_answer = str(callback.data.split('_')[1])
    if ctc_answer == 'add':
        pass
    if ctc_answer == 'delete':
        pass


@dp.callback_query_handler(lambda command: command.data and command.data.startswith('CP_'))
async def cp_add(callback: types.CallbackQuery):
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
