from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# from middlewares import TestMiddleware

import keyboards as kb

router = Router()

# router.message.outer_middleware(TestMiddleware())

class Reg(StatesGroup):
    name = State()
    phone = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello", reply_markup=kb.ikm1)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Help")

@router.message(Command("register"))
async def register(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("Введите имя")
@router.message(Reg.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.phone)
    await message.answer("Введите номер телефона")
@router.message(Reg.phone)
async def register_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await message.answer(f"Имя: {data["name"]}\nТелефон: {data["phone"]}")
    await state.clear()

@router.message(F.text == "aaa")
async def cmd_aaa(message: Message):
    await message.answer("Aaa")

@router.callback_query(F.data == "Aaa")
async def instagram(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_reply_markup(reply_markup=kb.ikm2)

