import requests

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import settings
from list_of_traceable_coins import all_coins

from sсhemas import Model

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings['TOKEN'])
dp = Dispatcher(bot=bot, storage=MemoryStorage())

basic_message = 'Choose the functionality you are interested in'

# inline keyboard buttons

# "Change tracked coins" buttons
inline_keyboard_ctc = InlineKeyboardMarkup(row_width=2)
inline_keyboard_ctc_buttons = [InlineKeyboardButton(text='🟢 ADD', callback_data='ctc_add'),
                               InlineKeyboardButton(text='🔴 DELETE', callback_data='ctc_delete')]
inline_keyboard_ctc.row(*inline_keyboard_ctc_buttons)

# "Check price" buttons
inline_keyboard_cp = InlineKeyboardMarkup(row_width=2)
inline_keyboard_cp_buttons = [InlineKeyboardButton(text='USD', callback_data='cp_usd'),
                              InlineKeyboardButton(text='EUR', callback_data='cp_eur'),
                              InlineKeyboardButton(text='RUB', callback_data='ctc_rub')]
inline_keyboard_cp.row(*inline_keyboard_ctc_buttons)


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

        "💱 Check price",
        "✍🏻 Change tracked coins",
        "📜 List of coins",
        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message,
                         reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "✍🏻 Change tracked coins")
async def currencies(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    for coin in all_coins:
        ch_coin = all_coins[coin][0]
        await message.answer(ch_coin,
                             reply_markup=keyboard)

    await message.reply('What to change?',
                        reply_markup=inline_keyboard_ctc)


@dp.message_handler(lambda message: message.text == "💱 Check price")
async def currencies(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer()

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

        await message.answer(coin_price,
                             reply_markup=keyboard)


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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
