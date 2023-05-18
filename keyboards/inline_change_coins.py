from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard_CTC = InlineKeyboardMarkup(row_width=2)
inline_keyboard_CTC_buttons = [
    InlineKeyboardButton(text="🟢 ADD", callback_data="CTC_add"),
    InlineKeyboardButton(text="🔴 DELETE", callback_data="CTC_delete"),
]
inline_keyboard_CTC.row(*inline_keyboard_CTC_buttons)
