from aiogram import (
    types,
    Dispatcher,
)

from imports import (
    dp,
    basic_message,
)


@dp.message_handler(lambda message: message.text == "🔙 Back" or "/start")
async def main_menu(message: types.Message) -> None:
    buttons = [
        "📊 Monitoring",
        "🏛 Wallet",
    ]

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    await message.answer(basic_message, reply_markup=keyboard)


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        main_menu, lambda message: message.text == "🔙 Back" or "/start"
    )
