from aiogram.types          import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def add_play_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Play", url="https://t.me/otvw_bot/test"))
    return keyboard.adjust(2).as_markup()
