from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command, Text

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from db import *

from loader import dp, bot

def main_menu():
	markup = InlineKeyboardMarkup(row_width=3)
	markup.insert(InlineKeyboardButton(text=f"Добавить товар",callback_data="add"))
	return markup



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
	await message.answer(text="Привет, я минибот.С Cлужу для того, чтобы добавлять товары в магазин @VapeLove_bot",reply_markup=main_menu)





