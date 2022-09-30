from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard_ctc = InlineKeyboardMarkup(row_width=2)
inline_keyboard_ctc_buttons = [InlineKeyboardButton(text='🟢 ADD', callback_data='ctc_add'),
                               InlineKeyboardButton(text='🔴 DELETE', callback_data='ctc_delete')]
inline_keyboard_ctc.row(*inline_keyboard_ctc_buttons)