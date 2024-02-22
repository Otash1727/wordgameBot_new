from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

mix_kb=InlineKeyboardMarkup(
    inline_keyboard=[
        InlineKeyboardButton(text='Join',callback_data='join1'),
        InlineKeyboardButton(text='start',callback_data='start1')
    ],
)