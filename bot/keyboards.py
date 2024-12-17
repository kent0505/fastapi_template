from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Каталог"),
        ],
        [
            KeyboardButton(text="Корзина"), 
            KeyboardButton(text="Контакты"),
        ],
    ],
    resize_keyboard=True, 
    input_field_placeholder="Aaa",
)

ikm1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Aaa", callback_data="Aaa"),
        ],
    ],
)

ikm2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bbb", callback_data="Bbb"),
            InlineKeyboardButton(text="Ccc", callback_data="Ccc"),
        ],
    ],
)