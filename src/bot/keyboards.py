from aiogram.types          import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def add_play_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Play", url="https://t.me/otvw_bot/test"))
    return keyboard.adjust(2).as_markup()



# main = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Каталог"),
#         ],
#         [
#             KeyboardButton(text="Корзина"), 
#             KeyboardButton(text="Контакты"),
#         ],
#     ],
#     resize_keyboard=True, 
#     input_field_placeholder="Aaa",
# )

# ikm1 = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(
#                 text="Play", 
#                 url="https://t.me/otvw_bot/test",
#                 # web_app=["https://t.me/otvw_bot/test"],
#             ),
#         ],
#     ],
# )




# ikm2 = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Bbb", callback_data="Bbb"),
#             InlineKeyboardButton(text="Ccc", callback_data="Ccc"),
#         ],
#     ],
# )