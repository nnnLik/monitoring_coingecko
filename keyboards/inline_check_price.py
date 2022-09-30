from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard_CP = InlineKeyboardMarkup(row_width=2)
inline_keyboard_CP_buttons = [InlineKeyboardButton(text='＄ - USD', callback_data='CP_usd'),
                              InlineKeyboardButton(text='€ - EUR', callback_data='CP_eur'),
                              InlineKeyboardButton(text='₽ - RUB', callback_data='CP_rub'), ]
inline_keyboard_CP.row(*inline_keyboard_CP_buttons)
