from aiogram           import Router
from aiogram.filters   import CommandStart
from aiogram.types     import Message

from src.bot.keyboards import *

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text="Hello", 
        reply_markup=await add_play_button()
    )

@router.message()
async def cmd_delete(message: Message):
    await message.delete()
