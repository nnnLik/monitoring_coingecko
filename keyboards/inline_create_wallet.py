from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard_CW = InlineKeyboardMarkup(row_width=2)
inline_keyboard_CW_buttons = [
    InlineKeyboardButton(text="👶 CREATE WALLET", callback_data="CREATE"),
]
inline_keyboard_CW.row(*inline_keyboard_CW_buttons)
