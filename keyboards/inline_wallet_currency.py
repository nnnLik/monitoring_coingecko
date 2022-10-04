from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard_WC = InlineKeyboardMarkup(row_width=2)
inline_keyboard_WC_buttons = [InlineKeyboardButton(text='＄ - USD', callback_data='WC_usd'),
                              InlineKeyboardButton(text='€ - EUR', callback_data='WC_eur'),
                              InlineKeyboardButton(text='₽ - RUB', callback_data='WC_rub'), ]
inline_keyboard_WC.row(*inline_keyboard_WC_buttons)
