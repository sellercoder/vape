from aiogram import types
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import Command, Text

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from db import *

from loader import dp, bot

def root_categories():
	markup = InlineKeyboardMarkup(row_width=3)
	for category in Category.all():
		markup.insert(InlineKeyboardButton(text=f"{category.undercategory}",callback_data=f"cat"))
	return markup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
	await message.answer("Категории",reply_markup=root_categories())





