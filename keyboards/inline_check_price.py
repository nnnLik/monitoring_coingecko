from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard_cp = InlineKeyboardMarkup(row_width=2)
inline_keyboard_cp_buttons = [InlineKeyboardButton(text='＄ - USD', callback_data='cp_usd'),
                              InlineKeyboardButton(text='€ - EUR', callback_data='cp_eur'),
                              InlineKeyboardButton(text='₽ - RUB', callback_data='cp_rub')]
inline_keyboard_cp.row(*inline_keyboard_cp_buttons)