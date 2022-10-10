import requests

from aiogram import (types,
                     Dispatcher, )

import data_base.sqlite_db
from keyboards.inline_change_coins import inline_keyboard_CTC
from keyboards.inline_check_price import inline_keyboard_CP

from coins_configs import (ALL_COINS,
                           LIST_OF_COINS, )

from schemas.sсhemas_current_price import MarketDataModel

from imports import (dp,
                     bot,
                     basic_message, )


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
async def tracked_coins(message: types.Message):
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
async def check_price(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer('Select the currency to which you want to see the coin price',
                         reply_markup=inline_keyboard_CP)


@dp.message_handler(lambda message: message.text == "📜 List of coins")
async def list_of_coins(message: types.Message):
    buttons = [

        "🔙 Back"

    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    coins_name_id = await data_base.sqlite_db.column_output()

    for coins_inf in coins_name_id:
        await message.answer(f'Coin Name: *{coins_inf[1]}*\nCoin ID: _{coins_inf[0]}_',
                             parse_mode="Markdown")


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


@dp.callback_query_handler(lambda command: command.data and command.data.startswith('CTC_'))
async def ctc_add(callback: types.CallbackQuery):
    ctc_answer = str(callback.data.split('_')[1])
    if ctc_answer == 'add':
        pass
    if ctc_answer == 'delete':
        pass


def register_monitoring_handlers(dp: Dispatcher):
    dp.register_message_handler(monitoring, lambda message: message.text == "📊 Monitoring")
    dp.register_message_handler(tracked_coins, lambda message: message.text == "✍🏻 Tracked coins")
    dp.register_message_handler(check_price, lambda message: message.text == "📈 Check price")
    dp.register_message_handler(cp_add, lambda command: command.data and command.data.startswith('CP_'))
    dp.register_message_handler(ctc_add, lambda command: command.data and command.data.startswith('CTC_'))