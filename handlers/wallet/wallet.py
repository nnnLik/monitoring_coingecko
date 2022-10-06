from aiogram import types, Dispatcher

from keyboards.inline_create_wallet import inline_keyboard_CW
from keyboards.inline_wallet_currency import inline_keyboard_WC

from data_base import sqlite_db
from data_base.sqlite_db import NoneUserWallet

from imports import (dp,
                     bot,
                     basic_message)


@dp.message_handler(lambda message: message.text == "🏛 Wallet")
async def wallet(message: types.Message):
    print(1)
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

        await message.answer(
            'To start work you need to __*create wallet*__',
            parse_mode="Markdown",
            reply_markup=inline_keyboard_CW)


@dp.callback_query_handler(lambda command: command.data and command.data.startswith('CREATE'))
async def create_wallet(callback: types.CallbackQuery):
    first_name = callback.from_user.first_name

    await bot.edit_message_text(
        text=f'Creation of a wallet for user {first_name} is in progress. In what currency will be your balance?',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=inline_keyboard_WC,
        parse_mode='html')


def register_wallet_handlers(dp: Dispatcher):
    dp.register_message_handler(wallet, text="🏛 Wallet")
    dp.register_message_handler(create_wallet, lambda command: command.data and command.data.startswith('CREATE'))